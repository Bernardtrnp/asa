import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { axiosInstance } from "@/lib/axios";

interface TestimoniData {
    rata_rata: number;
    total_rating: number;
    total_testimoni: number;
}

interface ApiResponse {
    data: TestimoniData;
    message: string;
    errors?: {
        [field: string]: string[];
    }
}

const useRataRataTestimoni = (
    limit: string | null,
    per_page: string | null,
    current_page: string | null
) => {
    const cacheKey = `testimoni-${limit}-${per_page}-${current_page}`;

    const initialETag = typeof window !== "undefined" ? localStorage.getItem(`${cacheKey}-etag`) : null;
    const initialCachedData = typeof window !== "undefined"
        ? JSON.parse(localStorage.getItem(`${cacheKey}-data`) || "null")
        : null;

    const [etag, setETag] = useState<string | null>(initialETag);
    const [cachedData, setCachedData] = useState<TestimoniData | null>(initialCachedData);

    return useQuery<ApiResponse>({
        queryKey: ["useRataRataTestimoni", limit, per_page, current_page],
        enabled: typeof window !== "undefined",
        queryFn: async () => {
            const headers: Record<string, string> = {
                "Content-Type": "application/json",
            };

            if (etag) headers["If-None-Match"] = etag;

            const response = await axiosInstance.get<ApiResponse>(
                `/rakit-app/store/profile`,
                {
                    headers,
                    validateStatus: () => true,
                }
            );

            if (response.status === 304 && cachedData) {
                return {
                    data: cachedData,
                    message: "From local cache (ETag matched)",
                };
            }

            if (response.status === 200) {
                const newETag = response.headers["etag"]; // lowercase "etag" untuk konsistensi
                const responseData = response.data.data;

                if (newETag && newETag !== etag) {
                    localStorage.setItem(`${cacheKey}-etag`, newETag);
                    setETag(newETag);
                }

                localStorage.setItem(`${cacheKey}-data`, JSON.stringify(responseData));
                setCachedData(responseData);

                return response.data;
            }

            throw new Error("Failed to fetch testimoni data");
        },
        staleTime: 0,
        refetchOnWindowFocus: false,
        retry: false,
    });
};

export { useRataRataTestimoni };
