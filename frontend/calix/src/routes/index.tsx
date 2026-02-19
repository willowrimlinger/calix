import {createFileRoute} from "@tanstack/react-router";
import {
    Center,
    Grid,
    Group,
    Paper,
    ScrollArea,
    Text,
    Title,
} from "@mantine/core";
import {DateTime} from "luxon";
import {useMemo} from "react";
import classes from "./index.module.css";
import {DOW, intToDOW} from "@/types/dow";

export const Route = createFileRoute("/")({
    component: App,
});

const begOfWeek: DOW.MON | DOW.SUN = DOW.MON;

interface DisplayDay {
    isToday: boolean;
    dateTime: DateTime;
    dow: DOW;
}

function App() {
    const today = DateTime.now();

    const displayDays = useMemo(() => {
        let startOfWeekDelta;
        if (begOfWeek === DOW.SUN) {
            startOfWeekDelta = today.weekday;
        } else {
            startOfWeekDelta = today.weekday - 1;
        }
        const startOfWeek = today.minus({days: startOfWeekDelta});

        const result: Array<DisplayDay> = [];

        for (let i = 0; i < 7; i++) {
            const currDay = startOfWeek.plus({days: i});
            result.push({
                isToday: currDay.startOf("day").equals(today.startOf("day")),
                dateTime: currDay,
                dow: intToDOW[currDay.weekday],
            });
        }

        return result;
    }, []);

    return (
        <Paper p="0">
            <Group
                gap="xl"
                align="center"
                h="2.25rem"
                p="xs"
            >
                <Title order={2}>Calix</Title>
            </Group>
            <Grid
                columns={7}
                gutter={0}
            >
                {displayDays.map((day, idx) => (
                    <Grid.Col
                        key={day.dateTime.toISO()}
                        span={1}
                        style={{
                            borderLeft: "1px none",
                            borderRight: idx === 6 ? "1px none" : undefined,
                        }}
                    >
                        <Group
                            align="baseline"
                            gap="0.25rem"
                            style={{
                                borderBottom: "1px solid #d0d0d0",
                            }}
                            h="calc(6px + 3.5rem)"
                        >
                            <Center
                                className={`
                                    ${classes.dateNumCircle}
                                    ${day.isToday ? classes.dateNumCircleToday : ""}
                                `}
                                ml="6px"
                                mb="6px"
                            >
                                {day.dateTime.get("day")}
                            </Center>
                            <Text>{day.dow.toLocaleUpperCase()}</Text>
                        </Group>
                    </Grid.Col>
                ))}
            </Grid>
            <ScrollArea
                style={{
                    height: "calc(100vh - 6px - 3.5rem - 2.25rem)",
                }}
            >
                <Group wrap="nowrap">
                    <div
                        style={{
                            display: "grid",
                        }}
                    >
                        {[...Array(24).keys()].map(i => (
                            <div>{i}</div>
                        ))}
                    </div>
                    <Grid
                        columns={7}
                        gutter={0}
                        style={{
                            flexGrow: 1,
                        }}
                    >
                        {displayDays.map((day, idx) => (
                            <Grid.Col
                                key={day.dateTime.toISO()}
                                span={1}
                                style={{
                                    borderLeft:
                                        "1px solid var(--mantine-color-gray-4)",
                                    borderRight:
                                        idx === 6
                                            ? "1px solid var(--mantine-color-gray-4)"
                                            : undefined,
                                }}
                            >
                                <div
                                    style={{
                                        display: "grid",
                                    }}
                                >
                                    {[...Array(24).keys()].map(i => (
                                        <div
                                            style={{
                                                height: "4rem",
                                            }}
                                        >
                                            {i}
                                        </div>
                                    ))}
                                </div>
                            </Grid.Col>
                        ))}
                    </Grid>
                </Group>
            </ScrollArea>
        </Paper>
    );
}
