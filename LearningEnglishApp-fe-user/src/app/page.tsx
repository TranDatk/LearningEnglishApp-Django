import MainSlider from "@/components/main/main.slider";
import { sendRequest } from "@/utils/api";
import { Container } from "@mui/material";

export default async function HomePage() {
  const res = await sendRequest<IBackendRes<ICourse[]>>({
    url: "http://127.0.0.1:8000/course/search-by-tag/",
    method: "POST",
    body: { "tags": ["TOEIC"] }
  })

  console.log(res)

  return (
    <Container>
      <MainSlider
        results={res?.results ?? []}
      />
    </Container>
  );
}
