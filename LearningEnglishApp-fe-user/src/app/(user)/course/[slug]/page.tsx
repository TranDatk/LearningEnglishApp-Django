import ListLesson from '@/components/course/list.lesson';
import { CardMedia, Container, Grid } from "@mui/material";
import MainContentCourse from '@/components/course/main.content.course';
import { getIdFromUrl, sendRequest } from '@/utils/api';
import CourseDescription from '@/components/course/course.description';
import Divider from '@mui/material/Divider';
import ThingsLearn from '@/components/course/things.learn';
import { Box } from "@mui/material";

const DetailCoursePage = async ({ params }: { params: { slug: string } }) => {

    const resCourse = await sendRequest<IBackendRes<ICourse>>({
        url: `${process.env.NEXT_PUBLIC_BACKEND_URL}/course/${getIdFromUrl(params.slug)}/`,
        method: 'GET',
    })

    const resLesson = await sendRequest<IBackendRes<ILesson[]>>({
        url: `${process.env.NEXT_PUBLIC_BACKEND_URL}/lesson/search-by-course/${getIdFromUrl(params.slug)}/`,
        method: 'GET',
        // headers: { 'Authorization': `Bearer ${session?.access_token}` },
    })

    return (
        <>
            <MainContentCourse course={resCourse?.results!} />
            <Container>
                <Grid container
                    spacing={2}
                    sx={{
                        display: "flex",
                        alignItems: "center",
                    }}>
                    <Grid md={8} xs={12}>
                        <Box sx={{ display: 'flex', gap: "2rem", flexDirection: "column" }}>
                            <ThingsLearn />
                            <Divider />
                            <CardMedia component="iframe"
                                src="https://www.youtube.com/embed/9ZuioBQXDV8?si=KMXOx8-HcdWMKh66"
                                sx={{
                                    aspectRatio: "16/9",
                                }}
                            />
                            <Divider />
                            <ListLesson lesson={resLesson?.results ?? []} />
                            <Divider />
                            <CourseDescription description={resCourse?.results != undefined ? resCourse?.results?.description : ""} />
                        </Box>
                    </Grid>
                    <Grid md={8} xs={12}>

                    </Grid>
                </Grid>


            </Container>
        </>
    )
}

export default DetailCoursePage;