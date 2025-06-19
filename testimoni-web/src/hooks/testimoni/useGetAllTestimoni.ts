import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { axiosInstance } from "@/lib/axios";
import { User } from "@/interfaces/User";
import { Testimoni } from "@/interfaces/Testimoni";

interface TestimoniData {
    testimoni: Testimoni;
    user: User;
}

interface PageInfo {
    current_page: number;
    current_item: TestimoniData[];
    items_per_page: number;
    limit: number;
    next_page: number | null;
    previous_page: number | null;
    total_items: number;
    total_pages: number;
}

interface ApiResponse {
    data: TestimoniData[];
    message: string;
    page: PageInfo;
    errors?: {
        [field: string]: string[];
    };
}

const useGetAllTestimoni = (
    limit: string | null,
    per_page: string | null,
    current_page: string | null
) => {
    const cacheKey = `testimoni-all-${limit}-${per_page}-${current_page}`;

    const initialETag = typeof window !== "undefined" ? localStorage.getItem(`${cacheKey}-etag`) : null;
    const initialCachedData = typeof window !== "undefined"
        ? JSON.parse(localStorage.getItem(`${cacheKey}-data`) || "null")
        : null;

    const [etag, setETag] = useState<string | null>(initialETag);
    const [cachedData, setCachedData] = useState<ApiResponse | null>(initialCachedData);

    return useQuery<ApiResponse>({
        queryKey: ["useGetAllTestimoni", limit, per_page, current_page],
        queryFn: async () => {
            const headers: Record<string, string> = {
                "Content-Type": "application/json",
            };

            if (etag) headers["If-None-Match"] = etag;

            const response = await axiosInstance.get<ApiResponse>("/rakit-app/testimoni", {
                headers,
                params: { limit, per_page, current_page },
                validateStatus: () => true,
            });

            if (response.status === 304 && cachedData) return cachedData;

            if (response.status === 200) {
                const newETag = response.headers["etag"];
                const newData = response.data;

                if (newETag && newETag !== etag) {
                    localStorage.setItem(`${cacheKey}-etag`, newETag);
                    setETag(newETag); // this won't retrigger now
                }

                localStorage.setItem(`${cacheKey}-data`, JSON.stringify(newData));
                setCachedData(newData);

                return newData;
            }

            throw new Error("Failed to fetch testimoni data");
        },
        enabled: typeof window !== "undefined",
        refetchOnWindowFocus: false,
        retry: false,
        staleTime: 0,
    });
};

export { useGetAllTestimoni };
