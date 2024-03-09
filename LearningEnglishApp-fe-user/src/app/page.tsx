import MainSlider from "@/components/main/main.slider";
import { sendRequest } from "@/utils/api";
import { Container } from "@mui/material";
import { getServerSession } from "next-auth/next";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";

export default async function HomePage() {
  const session = await getServerSession(authOptions);

  const res = await sendRequest<IBackendRes<ICourse[]>>({
    url: "http://127.0.0.1:8000/course/search-by-tag/",
    method: "POST",
    body: { "tags": ["TOEIC"] }
  })

  return (
    <Container>
      <MainSlider
        results={res?.results ?? []}
      />
    </Container>
  );
}
