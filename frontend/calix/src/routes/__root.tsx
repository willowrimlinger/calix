import {Outlet, createRootRoute} from "@tanstack/react-router";
import "@mantine/core/styles.css";
import {MantineProvider, createTheme} from "@mantine/core";

const theme = createTheme({
    /** Put your mantine theme override here */
});

export const Route = createRootRoute({
    component: () => (
        <MantineProvider theme={theme}>
            <Outlet />
        </MantineProvider>
    ),
});
