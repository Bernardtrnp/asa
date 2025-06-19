import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { axiosInstance } from "@/lib/axios";
import axios from "axios";

export async function middleware(request: NextRequest) {
    const url = request.nextUrl;
    const accessToken = request.cookies.get("accessToken")?.value;
    const clientETag = request.cookies.get("me-etag")?.value;
    const code = url.searchParams.get("code");

    if (accessToken) {
        try {
            const headers: Record<string, string> = {
                Authorization: `Bearer ${accessToken}`,
            };

            if (clientETag) {
                headers["If-None-Match"] = clientETag;
            }

            const responseUserMe = await axiosInstance.get(`/rakit-app/user/@me`, {
                headers,
                validateStatus: () => true,
            });
            const respUserMe = responseUserMe.data;

            if (responseUserMe.status === 304) {
                if (code) {
                    const searchParams = url.searchParams;
                    searchParams.delete("code");
                    url.search = searchParams.toString();
                    return NextResponse.redirect(url);
                }

                return NextResponse.next();
            }

            if (responseUserMe.status === 200) {
                const newETag = responseUserMe.headers["etag"];
                const url = request.nextUrl;
                const searchParams = url.searchParams;

                searchParams.delete("code");

                url.search = searchParams.toString();

                const response = NextResponse.redirect(url);

                if (newETag) {
                    response.cookies.set("me-etag", newETag, {
                        httpOnly: false,
                    });
                    response.cookies.set("me-data", JSON.stringify(respUserMe.data), {
                        httpOnly: false,
                    })
                }

                return response;
            }

            const response = NextResponse.next();
            response.cookies.delete("accessToken");
            response.cookies.delete("me-etag");
            return response;

        } catch (error: unknown) {
            if (axios.isAxiosError(error)) {
                if (error.response) {
                    console.error("❌ API Error Response:");
                    console.error("Status:", error.response.status);
                    console.error("Data:", error.response.data);
                } else {
                    console.error("❌ No response received from API.");
                }
            } else {
                console.error("❌ Unknown error:", error);
            }

            const response = NextResponse.next();
            response.cookies.delete("accessToken");
            response.cookies.delete("me-etag");
            return response;
        }
    }

    if (code) {
        try {
            const response = await axios.post(
                `${process.env.NEXT_PUBLIC_USER_API}/rakit-app/auth/login`,
                {
                    code,
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
            const resp = response.data;
            if (response.status === 201) {
                const response = NextResponse.next();
                response.cookies.set("accessToken", resp.token.access_token, {
                    httpOnly: false,
                });
                return response;
            }
        } catch {
            // 
        }
    }

    return NextResponse.next();
}

export const config = {
    matcher: [
        "/",
    ],
};
