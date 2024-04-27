// NewChatModal.js
import React, { useState } from 'react';
import './NewChatModal.css';

const NewChatModal = ({ onAddChat, onCloseModal }) => {
  const [chatId, setChatId] = useState('');

  const handleChange = (event) => {
    setChatId(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Здесь можно выполнить дополнительные действия, например, валидацию или отправку данных на бэкэнд
    onAddChat(chatId);
  };

  return (
    <div className="modal-background">
      <div className="modal-container">
        <button className="close-button" onClick={onCloseModal}>x</button>
        <h2>Новый чат</h2>
        <form onSubmit={handleSubmit}>
          <label>
            ID чата:
            <input type="text" value={chatId} onChange={handleChange} />
          </label>
          <button type="submit">Создать</button>
        </form>
      </div>
    </div>
  );
};

export default NewChatModal;
