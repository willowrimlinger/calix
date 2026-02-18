import {createFileRoute} from "@tanstack/react-router";
import {Center, Grid, Group, Paper, Text, Title} from "@mantine/core";
import {DateTime} from "luxon";
import {useMemo} from "react";
import classes from "./index.module.css";
import {DOW, intToDOW} from "@/types/event";

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
        <Paper p="sm">
            <Group
                gap="xl"
                align="center"
            >
                <Title order={2}>Calix</Title>
            </Group>
            <Grid columns={7}>
                {displayDays.map(day => (
                    <Grid.Col span={1}>
                        <Group
                            align="baseline"
                            gap="0.25rem"
                        >
                            <Center
                                className={`
                                    ${classes.dateNumCircle}
                                    ${day.isToday ? classes.dateNumCircleToday : ""}
                                `}
                            >
                                {day.dateTime.get("day")}
                            </Center>
                            <Text>{day.dow.toLocaleUpperCase()}</Text>
                        </Group>
                    </Grid.Col>
                ))}
            </Grid>
        </Paper>
    );
}
