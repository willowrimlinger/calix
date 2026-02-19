import type { ILabel } from "./label"
import type { IRecurrence } from "./recurrence"

export interface IEvent {
    id: number
    start: string
    end: string
    description: string
    location: string
    recurrence: IRecurrence
    label: ILabel
}
