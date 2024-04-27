import axios from "axios";

const apiInstance = axios.create({baseURL: import.meta.env.VITE_API_URL});

export const api = {
    getChats: () => apiInstance.get('/chats'),
    sendMessage: (chatId, message) => apiInstance.post(`/chats/${chatId}/messages`, {message}),
    addChat: (newChatName) => apiInstance.post('/chats', { name: newChatName }),
    getChatMessages: (chatId) => apiInstance.get(`/chats/${chatId}/messages`),
    getChatMetrics: (chatId) => apiInstance.get(`/chats/${chatId}/metrics`),
}
