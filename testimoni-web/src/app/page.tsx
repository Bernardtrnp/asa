'use client'
import Image from "next/image";
import BannerPage1 from "@/../public/banner.png";
import BannerPage2 from "@/../public/1448x520-HB-OVO-Juni.png";
import BannerPage3 from "@/../public/LG-1448x520-HB-Shopeepay_Juni.png";
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
  CardContent
} from "@/components/ui/card"
import { Separator } from "@/components/ui/separator";
import { FaDiscord } from "react-icons/fa";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { FaStar } from "react-icons/fa";
import { FaGlobe } from "react-icons/fa";
import React, { useState, useRef, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"
import Cookies from "js-cookie";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { IoExitOutline } from "react-icons/io5";
import { useFormik } from "formik";
import axios from "axios";
import { IoLinkOutline } from "react-icons/io5";
import { useGetAllTestimoni } from "@/hooks/testimoni/useGetAllTestimoni";
import { useRataRataTestimoni } from "@/hooks/testimoni/useRataRataTestimoni";
import dayjs from 'dayjs';
import { FadeLoader } from "react-spinners";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { toast } from "sonner"
import type { User } from "@/interfaces/User";
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { FaWhatsapp } from "react-icons/fa";

interface ModeToggleProps {
  setTheme: (theme: "light" | "dark" | "system") => void;
}

export const ModeToggle: React.FC<ModeToggleProps> = ({ setTheme }) => {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="icon">
          <Sun className="h-[1.2rem] w-[1.2rem] scale-100 rotate-0 transition-all dark:scale-0 dark:-rotate-90" />
          <Moon className="absolute h-[1.2rem] w-[1.2rem] scale-0 rotate-90 transition-all dark:scale-100 dark:rotate-0" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => setTheme("light")}>
          Light
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("dark")}>
          Dark
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("system")}>
          System
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}



export default function Home() {
  const accessToken = Cookies.get("accessToken");
  const [userMe, setUserMe] = useState<User | null>(null);
  const { setTheme } = useTheme()

  useEffect(() => {
    const userMeCookie = Cookies.get("me-data");
    if (userMeCookie) {
      try {
        const parsed = JSON.parse(userMeCookie) as User;
        setUserMe(parsed);
      } catch (e) {
        console.error("❌ Gagal parse me-data cookie:", e);
      }
    }
  }, []);

  const inputRef = useRef<HTMLInputElement>(null)
  const [fileName, setFileName] = useState<string>("No file chosen")

  const { data: testimoniRataRata, isLoading: testimoniRataRataIsLoading } = useRataRataTestimoni(null, null, null);

  const formik = useFormik({
    initialValues: {
      rating: '',
      description: '',
      proof: null as File | null,
    },
    onSubmit: async (values, { resetForm }) => {
      const formData = new FormData();
      formData.append('rating', values.rating);
      formData.append('description', values.description);
      if (values.proof) formData.append('proof', values.proof);

      try {
        await axios.post(
          `${process.env.NEXT_PUBLIC_USER_API}/rakit-app/testimoni`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'multipart/form-data',
            },
          }
        );
        setIsOpen(false);
        setFileName("No file chosen");
        resetForm();
        toast.success('success add vouch')
      } catch {
        toast.error('error add vouch')
      }
    },
  });

  const triggerFileSelect = () => {
    inputRef.current?.click()
  }

  const [isOpen, setIsOpen] = useState(false);

  const handleLogin = () => {
    if (accessToken) {
      setIsOpen(true);
    } else {
      window.location.href = `${process.env.NEXT_PUBLIC_OAUTH_URL}`;
    }
  };

  const handleLogout = async () => {
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_USER_API}/rakit-app/auth/logout`,
        {},
        {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      if (response.status === 201) {
        Cookies.remove("accessToken");
        Cookies.remove("me-etag");
        localStorage.removeItem("me-data");
        localStorage.removeItem("me-etag");
        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i);
          if (key && key.startsWith("testimoni-")) {
            localStorage.removeItem(key);
            i--;
          }
        }
        setIsOpen(false);
        toast.success('success logout')
      }
    } catch (error) {
      console.error("Logout error:", error);
      toast.error('failed logout')
    }
  };

  return (
    <div className="min-h-screen bg-[#e0f0ff] dark:bg-[#111] py-5">
      <Carousel className="lg:w-[85%] md:w-[85%] sm:w-[80%] w-[55%] mx-auto" opts={{ loop: true }}>
        <CarouselContent className="text-black">
          <CarouselItem>
            <div className="w-full h-[200px] overflow-hidden rounded-md">
              <Image
                src={BannerPage1}
                alt="Banner"
                className="w-full h-full object-cover"
              />
            </div>
          </CarouselItem>
          <CarouselItem>
            <div className="w-full h-[200px] overflow-hidden rounded-md">
              <Image
                src={BannerPage2}
                alt="Banner"
                className="w-full h-full object-cover"
              />
            </div>
          </CarouselItem>
          <CarouselItem>
            <div className="w-full h-[200px] overflow-hidden rounded-md">
              <Image
                src={BannerPage3}
                alt="Banner"
                className="w-full h-full object-cover"
              />
            </div>
          </CarouselItem>
        </CarouselContent>
        <CarouselPrevious style={{ color: "white", backgroundColor: "#3D4042", opacity: 1 }} className="cursor-pointer" />
        <CarouselNext style={{ color: "white", backgroundColor: "#3D4042", opacity: 1 }} className="cursor-pointer" />
      </Carousel>

      <div className="flex flex-col lg:flex-row gap-5 lg:w-[85%] md:w-[85%] sm:w-[80%] w-[55%] mx-auto mt-6">
        <div className="flex flex-col gap-5 w-full lg:w-[30%]">
          <Card className="card-1 text-center shadow-none border-none bg-white dark:bg-[#1f1f1f]">
            <CardHeader>
              <Image
                src={BannerPage1}
                alt="Banner"
                className="w-[100px] h-[100px] rounded-full mx-auto object-cover"
              />
              <CardTitle className="mt-5 text-black dark:text-white">Joshh Store</CardTitle>
              <CardDescription>Best Seller</CardDescription>
            </CardHeader>
            {testimoniRataRataIsLoading === false ? (
              <CardFooter className="flex-col">
                <p className="mx-auto text-black dark:text-white">{`Score: ${testimoniRataRata?.data.rata_rata || 0} / 5.0 from ${testimoniRataRata?.data.total_testimoni ? testimoniRataRata?.data.total_testimoni : 0} vouches`}</p>
                <Separator className="mt-3 bg-gray-200" />
                <div className="flex flex-row justify-center items-center gap-3 mt-3 text-black dark:text-white">
                  <Link href="https://discord.gg/TerXnRXkQt">
                    <FaDiscord size={25} />
                  </Link>
                  <Link href="https://n54m2rj9-3000.asse.devtunnels.ms/">
                    <FaGlobe size={20} />
                  </Link>
                  <Link href="https://n54m2rj9-3000.asse.devtunnels.ms/">
                    <FaWhatsapp size={20} />
                  </Link>
                </div>
              </CardFooter>
            ) : ''}
          </Card>
        </div>
        <div className="w-full lg:w-[70%] flex flex-col">
          <div className="flex flex-row items-center justify-end mb-4">
            <ModeToggle setTheme={setTheme} />
            <Button className="bg-[#2B2D2E] text-white hover:bg-[#2B2D2E]/90 cursor-pointer ml-2" onClick={handleLogin}>
              Add Vouch
            </Button>
          </div>
          <ThreeColumnCardList />
        </div>
      </div>
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="bg-white text-black dark:bg-[#1f1f1f] dark:text-white">
          <DialogHeader>
            <DialogTitle className="ms-2">
              <div className="flex flex-col gap-2">
                <p>Add a vouch for stockx24</p>
                <hr className="mt-1 me-2" />
                <div className="flex justify-between items-center mt-0.5">
                  <div className="flex flex-row">
                    <FaDiscord size={20} className="me-2" />
                    <p className="text-sm">{`Logged in as: ${userMe?.username}`}</p>
                  </div>
                  <div className="flex flex-row me-2 cursor-pointer" onClick={() => handleLogout()}>
                    <IoExitOutline size={20} className="text-red-500" />
                    <p className="text-sm ms-1 font-semibold text-red-500">Logout</p>
                  </div>
                </div>
              </div>
            </DialogTitle>
            <DialogDescription>
              <form className="mt-5" onSubmit={formik.handleSubmit}>
                <div className="flex flex-col gap-4 justify-center items-center">
                  <Select
                    onValueChange={(val) => formik.setFieldValue('rating', val)}
                  >
                    <SelectTrigger className="w-full max-w-md border border-gray-200">
                      <SelectValue placeholder="Rating" />
                    </SelectTrigger>
                    <SelectContent className="w-full max-w-md bg-gray-50">
                      {[1, 2, 3, 4, 5].map((n) => (
                        <SelectItem key={n} value={String(n)}>
                          {[...Array(n)].map((_, i) => (
                            <FaStar key={i} className="text-yellow-500 inline-block" />
                          ))}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>

                  <Textarea
                    placeholder="Vouch content"
                    className="max-w-md w-full border border-gray-200"
                    name="description"
                    value={formik.values.description}
                    onChange={formik.handleChange}
                  />

                  <div className="border border-gray-200 rounded-md px-3 py-2 flex items-center space-x-3 overflow-hidden max-w-md w-full">
                    <input
                      ref={inputRef}
                      type="file"
                      className="hidden"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        setFileName(file ? file.name : "No file chosen");
                        formik.setFieldValue('proof', file);
                      }}
                    />
                    <Button type="button" onClick={triggerFileSelect} variant="secondary" className="shrink-0 bg-blue-500 text-white hover:bg-blue-500/90">
                      Choose File
                    </Button>
                    <div className="flex-1 overflow-hidden">
                      <p className=" text-sm text-muted-foreground">{fileName}</p>
                    </div>
                  </div>

                  <div className="flex w-full justify-end me-3">
                    <Button type="submit" className="bg-[#2B2D2E] text-white hover:bg-[#2B2D2E]/90 cursor-pointer">
                      Submit
                    </Button>
                  </div>
                </div>
              </form>
            </DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    </div>
  );
}

const ThreeColumnCardList = () => {
  const searchParams = useSearchParams();
  const router = useRouter();

  const pageParam = searchParams.get("current_page") || "1";
  const currentPage = parseInt(pageParam, 10);
  const itemsPerPage = 9;

  const { data: dataAllTestimoni, isLoading: isLoadingDataAllTestimoni, error: errorDataAllTestimoni } = useGetAllTestimoni(null, itemsPerPage.toString(), pageParam);
  if (isLoadingDataAllTestimoni) {
    return (
      <div className="flex justify-center items-center h-[500px] w-full">
        <FadeLoader color="#2B2D2E" />
      </div>
    );
  }
  if (errorDataAllTestimoni) return;

  const totalPages = dataAllTestimoni?.page?.total_pages || 1;
  const testimonials = dataAllTestimoni?.page?.current_item || [];

  const handlePageChange = (newPage: number) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set("current_page", newPage.toString());
    router.push(`?${params.toString()}`, { scroll: false });
  };

  const renderPaginationItems = () => {
    const pages = [];

    pages.push(
      <PaginationItem key="prev">
        <PaginationPrevious
          onClick={() => currentPage > 1 && handlePageChange(currentPage - 1)}
          className="bg-[#3D4042] text-white rounded-md cursor-pointer"
        />
      </PaginationItem>
    );

    if (totalPages <= 5) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(
          <PaginationItem key={i}>
            <PaginationLink
              onClick={() => handlePageChange(i)}
              className={`rounded-md cursor-pointer px-3 py-1 ${currentPage === i ? "bg-blue-600 text-white" : "bg-[#3D4042] text-white"
                }`}
            >
              {i}
            </PaginationLink>
          </PaginationItem>
        );
      }
    } else {
      pages.push(
        <PaginationItem key={1}>
          <PaginationLink
            onClick={() => handlePageChange(1)}
            className={`rounded-md cursor-pointer px-3 py-1 ${currentPage === 1 ? "bg-blue-600 text-white" : "bg-[#3D4042] text-white"
              }`}
          >
            1
          </PaginationLink>
        </PaginationItem>
      );

      if (currentPage > 3) {
        pages.push(<PaginationEllipsis key="start-ellipsis" className="bg-[#3D4042] text-gray-400 rounded-md cursor-pointer" />);
      }

      for (
        let i = Math.max(2, currentPage - 1);
        i <= Math.min(totalPages - 1, currentPage + 1);
        i++
      ) {
        pages.push(
          <PaginationItem key={i}>
            <PaginationLink
              onClick={() => handlePageChange(i)}
              className={`rounded-md cursor-pointer px-3 py-1 ${currentPage === i ? "bg-blue-600 text-white" : "bg-[#3D4042] text-white"
                }`}
            >
              {i}
            </PaginationLink>
          </PaginationItem>
        );
      }

      if (currentPage < totalPages - 2) {
        pages.push(<PaginationEllipsis key="end-ellipsis" className="bg-[#3D4042] text-gray-400 rounded-md cursor-pointer" />);
      }

      pages.push(
        <PaginationItem key={totalPages}>
          <PaginationLink
            onClick={() => handlePageChange(totalPages)}
            className={`rounded-md cursor-pointer px-3 py-1 ${currentPage === totalPages ? "bg-blue-600 text-white" : "bg-[#3D4042] text-white"
              }`}
          >
            {totalPages}
          </PaginationLink>
        </PaginationItem>
      );
    }

    pages.push(
      <PaginationItem key="next">
        <PaginationNext
          onClick={() => currentPage < totalPages && handlePageChange(currentPage + 1)}
          className="bg-[#3D4042] text-white rounded-md cursor-pointer"
        />
      </PaginationItem>
    );

    return pages;
  };


  return (
    <>
      <div
        className="max-h-[550px] overflow-y-auto w-full"
        style={{ scrollbarWidth: "none", msOverflowStyle: "none" }}
      >
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {testimonials.map((testimonial) => (
            <Card
              key={testimonial.testimoni.id}
              className="w-full bg-white border-none shadow-none dark:bg-[#1f1f1f] animate-fadeInUp 
              duration-350 ease-in-out 
              hover:-translate-y-3 hover:shadow-lg mt-3"
            >
              <CardHeader>
                <CardTitle>
                  <div className="flex flex-row items-center gap-2">
                    <Image
                      src={testimonial.user.avatar}
                      width={25}
                      height={25}
                      alt="Avatar"
                      className="w-[25px] h-[25px] rounded-full object-cover border-blue-500 border-2"
                    />
                    <Link
                      href={`https://discord.dog/${testimonial.user.discord_id}`}
                      className="underline text-black dark:text-white flex flex-row gap-1"
                    >
                      <p className="text-blue-500">{testimonial.user.username}</p>
                      <Tooltip>
                        <TooltipTrigger>
                          <p className="hover:text-gray-800 dark:hover:text-gray-200 lg:truncate lg:max-w-[100px] sm:truncate sm:max-w-[150px] xl:truncate xl:max-w-[250px]">
                            ({testimonial.user.discord_id})
                          </p>
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>({testimonial.user.discord_id})</p>
                        </TooltipContent>
                      </Tooltip>
                    </Link>
                  </div>
                </CardTitle>
              </CardHeader>

              <CardContent className="flex flex-col gap-1.5 text-black ">
                <div className="flex flex-row gap-1 items-center dark:text-yellow-500">
                  {[...Array(testimonial.testimoni.rating)].map((_, i) => (
                    <FaStar key={i} />
                  ))}
                  <p className="ms-1">({testimonial.testimoni.rating}/5)</p>
                </div>
                <p className="dark:text-white">{testimonial.testimoni.description}</p>

                {testimonial.testimoni.url_testimoni && (
                  <Link
                    href={testimonial.testimoni.url_testimoni}
                    target="_blank"
                    className="underline font-semibold flex items-center gap-1.5 cursor-pointer dark:text-white"
                  >
                    <p>view proof</p>
                    <IoLinkOutline size={20} className="mt-1" />
                  </Link>
                )}
              </CardContent>

              <CardFooter>
                <div className="flex justify-between w-full text-sm text-gray-400">
                  <Tooltip>
                    <TooltipTrigger>
                      <p className="sm:truncate sm:max-w-[150px] hidden sm:block xl:truncate xl:max-w-[250px] lg:truncate lg:max-w-[130px] md:truncate md:max-w-[200px]">{testimonial.testimoni.id}</p>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>{testimonial.testimoni.id}</p>
                    </TooltipContent>
                  </Tooltip>
                  <Tooltip>
                    <TooltipTrigger>
                      <p className="sm:truncate sm:max-w-[50px] hidden sm:block xl:truncate xl:max-w-[250px] lg:truncate lg:max-w-[105px] md:truncate md:max-w-[100px]">
                        {dayjs(testimonial.testimoni.created_at).format("DD-MM-YYYY HH:mm")}
                      </p>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>{dayjs(testimonial.testimoni.created_at).format("DD-MM-YYYY HH:mm")}</p>
                    </TooltipContent>
                  </Tooltip>
                </div>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>

      {!isLoadingDataAllTestimoni && Array.isArray(testimonials) && testimonials.length > 0 && (
        <Pagination className="mt-4 hidden sm:flex">
          <PaginationContent>{renderPaginationItems()}</PaginationContent>
        </Pagination>
      )}
    </>
  );
};
