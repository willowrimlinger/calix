export enum DOW {
    MON = "mon",
    TUE = "tue",
    WED = "wed",
    THU = "thu",
    FRI = "fri",
    SAT = "sat",
    SUN = "sun",
}

export const intToDOW = {
    1: DOW.MON,
    2: DOW.TUE,
    3: DOW.WED,
    4: DOW.THU,
    5: DOW.FRI,
    6: DOW.SAT,
    7: DOW.SUN,
};

export const DOWtoInt = {
    [DOW.MON]: 1,
    [DOW.TUE]: 2,
    [DOW.WED]: 3,
    [DOW.THU]: 4,
    [DOW.FRI]: 5,
    [DOW.SAT]: 6,
    [DOW.SUN]: 7,
};

export const DOWs = Object.values(DOW);

