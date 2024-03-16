import ListSubheader from '@mui/material/ListSubheader';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Collapse from '@mui/material/Collapse';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import DraftsIcon from '@mui/icons-material/Drafts';
import SendIcon from '@mui/icons-material/Send';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import StarBorder from '@mui/icons-material/StarBorder';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import ListLesson from '@/components/course/list.lesson';
import { Container } from "@mui/material";
import MainContentCourse from '@/components/course/main.content.course';
import { getIdFromUrl, sendRequest } from '@/utils/api';
import CourseDescription from '@/components/course/course.description';

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
    console.log(resCourse?.results != undefined && resCourse?.results?.description)

    return (
        <>
            <MainContentCourse course={resCourse?.results!} />
            <Container>
                <ListLesson lesson={resLesson?.results ?? []} />
                <CourseDescription description={resCourse?.results != undefined && resCourse?.results?.description} />
            </Container>
        </>
    )
}

export default DetailCoursePage;