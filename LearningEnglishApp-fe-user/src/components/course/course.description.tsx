import { Box } from "@mui/material";

interface IProps {
    description: React.ReactNode
}

export default function CourseDescription(props: IProps): React.ReactNode {
    return (
        <Box>
            {props?.description}
        </Box>
    );
}

