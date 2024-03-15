import Container from "@mui/material/Container";
import PauseIcon from '@mui/icons-material/Pause';

interface IProps {
    course: ICourse;
}

const MainContentCourse = (props: IProps) => {
    return (
        <div style={{ marginTop: 20 }}>
            <div
                style={{
                    padding: 20,
                    height: 400,
                    background: "linear-gradient(135deg, rgb(106, 112, 67) 0%, rgb(11, 15, 20) 100%)"
                }}
            >
                <Container sx={{ display: "flex", gap: 15, height: "100%" }}>
                    <div className="left"
                        style={{
                            width: "60%",
                            height: "calc(100% - 10px)",
                            display: "flex",
                            flexDirection: "column",
                            justifyContent: "space-between"
                        }}
                    >
                        <div className="info" style={{ display: "flex" }}>
                            <div>
                                <div
                                    style={{
                                        borderRadius: "50%",
                                        background: "#f50",
                                        height: "50px",
                                        width: "50px",
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "center",
                                        cursor: "pointer"
                                    }}
                                >
                                    <PauseIcon
                                        sx={{ fontSize: 30, color: "white" }}
                                    />
                                </div>
                            </div>
                            <div style={{ marginLeft: 20 }}>
                                <div style={{
                                    padding: "0 5px",
                                    background: "#333",
                                    fontSize: 30,
                                    width: "fit-content",
                                    color: "white"
                                }}>
                                    {props.course?.name}
                                </div>
                                <div style={{
                                    padding: "0 5px",
                                    marginTop: 10,
                                    background: "#333",
                                    fontSize: 20,
                                    width: "fit-content",
                                    color: "white"
                                }}
                                >
                                    Eric
                                </div>
                            </div>
                        </div>
                        <div>
                            khong co gi
                        </div>
                    </div>
                    <div className="right"
                        style={{
                            width: "25%",
                            padding: 15,
                            display: "flex",
                            alignItems: "center"
                        }}
                    >
                        <div style={{
                            background: "#ccc",
                            width: 250,
                            height: 250
                        }}>
                        </div>
                    </div>
                </Container>
            </div>
        </div>
    )
}

export default MainContentCourse;