import {Outlet, createRootRoute} from "@tanstack/react-router";
import "@mantine/core/styles.css";
import {MantineProvider, createTheme} from "@mantine/core";
import type {MantineColorsTuple} from "@mantine/core";

const accent: MantineColorsTuple = [
    "#e8fcef",
    "#d9f3e2",
    "#b6e4c5",
    "#8fd4a6",
    "#6fc78b",
    "#59bf7a",
    "#46b86b",
    "#3da55f",
    "#329353",
    "#227f44",
];

const theme = createTheme({
    colors: {
        accent: accent,
    },
    autoContrast: true,
});

export const Route = createRootRoute({
    component: () => (
        <MantineProvider theme={theme}>
            <Outlet />
        </MantineProvider>
    ),
});
