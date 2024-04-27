import React, { useState, useEffect } from 'react';
import './ChatList.css';
import NewChatModal from './NewChatModal';
import { api } from './api';

const ChatList = ({ onSelectChat }) => {
  const [showModal, setShowModal] = useState(false);
  const [chats, setChats] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const {data} = await api.getChats()
        setChats(data);
      } catch (error) {
        console.error('Ошибка при загрузке чатов:', error);
        setErrorMessage('Ошибка при загрузке чатов');
      }
    };

    fetchChats();
  }, []);

  const handleOpenModal = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setErrorMessage('');
  };

  const handleAddChat = async (newChatName) => {
    try {
      // Отправляем запрос на бэкенд для добавления нового чата
      const { data } = await api.addChat(newChatName);
      if (data.success) {
        // Если чат успешно добавлен на сервере, обновляем список чатов
        setChats(prevChats => [...prevChats, { id: data.chatId, name: newChatName, isFavorite: false }]);
        setShowModal(false);
      } else {
        setErrorMessage('Ошибка при добавлении нового чата');
      }
    } catch (error) {
      console.error('Ошибка при добавлении нового чата:', error);
      setErrorMessage('Ошибка при добавлении нового чата');
    }
  };

  const handleChatClick = (chatId) => {
    onSelectChat(chatId); // Передача chatId родительскому компоненту
  };

  return (
    <div className="chat-list">
      <div className="chati">
        <h2>Чаты</h2>
        <button className="novi" onClick={handleOpenModal}></button>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
      </div>
      {showModal && <NewChatModal onAddChat={handleAddChat} onCloseModal={handleCloseModal} />}
      {chats.map(chat => (
        <div key={chat.id} className="chat-item" onClick={() => handleChatClick(chat.id)}>
          <p>{chat.name}</p>
          {chat.isFavorite && <span>Избранное</span>}
        </div>
      ))}
    </div>
  );
};

export default ChatList;
