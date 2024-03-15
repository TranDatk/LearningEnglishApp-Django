'use client'
import * as React from 'react';
import { styled } from '@mui/material/styles';
import ArrowForwardIosSharpIcon from '@mui/icons-material/ArrowForwardIosSharp';
import MuiAccordion, { AccordionProps } from '@mui/material/Accordion';
import MuiAccordionSummary, {
    AccordionSummaryProps,
} from '@mui/material/AccordionSummary';
import MuiAccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Box from '@mui/material/Box';

interface IProps {
    lesson: ILesson[];
}

const Accordion = styled((props: AccordionProps) => (
    <MuiAccordion disableGutters elevation={0} square {...props} />
))(({ theme }) => ({
    border: `1px solid ${theme.palette.divider}`,
    '&:not(:last-child)': {
        borderBottom: 0,
    },
    '&::before': {
        display: 'none',
    },
}));


const AccordionSummary = styled((props: AccordionSummaryProps) => (
    <MuiAccordionSummary
        expandIcon={<ArrowForwardIosSharpIcon sx={{ fontSize: '0.9rem' }} />}
        {...props}
    />
))(({ theme }) => ({
    backgroundColor:
        theme.palette.mode === 'dark'
            ? 'rgba(255, 255, 255, .05)'
            : 'rgba(0, 0, 0, .03)',
    flexDirection: 'row-reverse',
    '& .MuiAccordionSummary-expandIconWrapper.Mui-expanded': {
        transform: 'rotate(90deg)',
    },
    '& .MuiAccordionSummary-content': {
        marginLeft: theme.spacing(1),
    },
}));


const AccordionDetails = styled(MuiAccordionDetails)(({ theme }) => ({
    padding: theme.spacing(2),
    borderTop: '1px solid rgba(0, 0, 0, .125)',
}));

const ListLesson = (props: IProps) => {
    const [expanded, setExpanded] = React.useState(false);


    const handleExpansion = () => {
        setExpanded((prevExpanded) => !prevExpanded);
    };

    return (
        <div>
            {Array.isArray(props?.lesson) && props?.lesson.map(lesson => {
                return (
                    <Accordion id={lesson?.id.toString()}>
                        <AccordionSummary
                            aria-controls={`panel-${lesson?.id}-content`}
                            id={`panel-${lesson?.id}-header`}>
                            <Typography>
                                {lesson?.name}
                            </Typography>
                            <Typography sx={{ ml: 'auto' }}>
                                {props.lesson.length - 1}
                            </Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <blockquote style={{
                                borderLeft: "4px solid rgb(206, 208, 212)",
                                paddingLeft: "10px"
                            }}>
                                {lesson?.description}
                            </blockquote>
                            <Typography>
                                Lorem
                            </Typography>
                        </AccordionDetails>
                    </Accordion>
                )
            })}



        </div >
    );
}

export default ListLesson;