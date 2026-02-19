export enum RecurrenceType {
    DOW = "dow",
    DOM = "dom",
    DAY = "day",
    WEEK = "week",
    MONTH = "month",
    YEAR = "year",
}

export interface IRecurrence {
    id: number
    n: number
    type: RecurrenceType
    start_date: string
    end_date: string
}
