import { createFileRoute } from '@tanstack/react-router'
import { Title } from '@mantine/core'

export const Route = createFileRoute('/')({
  component: App,
})

function App() {
  return <Title order={1}>Calix</Title>
}
