import {createFileRoute} from "@tanstack/react-router";
import {Grid, Group, Paper, Title} from "@mantine/core";
import {DateTime} from "luxon";
import { DOWs } from "@/types/event";

export const Route = createFileRoute("/")({
    component: App,
});

function App() {
    const today = DateTime.now()
    return (
        <Paper p="sm">
            <Group gap="xl" align="center">
                <Title order={1}>Calix</Title>
            </Group>
            <Grid columns={7}>
                {DOWs.map(dow => (
                    <Grid.Col span={1}>
                        <Title order={3}>{dow}</Title>
                    </Grid.Col>
                ))}
            </Grid>
        </Paper>
    );
}
