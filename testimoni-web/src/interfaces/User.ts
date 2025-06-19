export interface User {
    id: string
    username: string
    email: string | null
    is_active: boolean
    updated_at: number
    created_at: number
    provider: string
    avatar: string
    discord_id: number
    api_key: string | null
}