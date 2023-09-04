import React, { useState, useEffect, useRef, useContext }  from 'react'
import { scrollToElement, scrollDown } from '../../utils/ScrollDown';
import AuthContext from '../../context/AuthContext';
import useAxios from '../../utils/useAxios';
import ChatRoomMessage from './ChatRoomMessage.jsx';
import TimestampToTimezone from "../../utils/timestampToTimezone.js";
import addUnreadTitle from "../../utils/addTitle";
import {VscSend} from 'react-icons/vsc'
import {MdOutlineAddAPhoto} from 'react-icons/md';

function PageChats({ selectedChat }) {
  const chatSocket = useRef();
  const [connected, setConnected] = useState(false);
  const [toScrollDown, setToScrollDown] = useState(false);

  const [isTyping, setIsTyping] = useState(false);
  const [timerId, setTimerId] = useState(null)
  const [companion, setCompanion] = useState({})
  const [isCompanionTyping, setIsCompanionTyping] = useState(false);

  const [messageInput, setMessageInput] = useState('');
  const [fileInput, setFileInput] = useState(null);
  const [chatMessages, setChatMessages] = useState([]);

  const {user, accessToken} = useContext(AuthContext);
  const api = useAxios();



  async function fetchMessages() {
    let response = await api.get(`api/v1/chat/${selectedChat.id}/messages/`);
    if (response.status === 200){
      return response.data;
    }
  }

  function newWebSocket(chat_id){
    let url = `ws://localhost:8000/ws/socket-server/chat/${accessToken}/${chat_id}/`

    if (chatSocket.current) {
      if (chatSocket.current.url !== url) {
        chatSocket.current.close();
      }
    }
    return new WebSocket(url);
  }

  function loadWebSocket(chat_id){
    chatSocket.current = newWebSocket(chat_id);

    chatSocket.current.onopen = () => {
      setConnected(true);
      console.log('Socket connected');
    }

    chatSocket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log(data)
      if(data.type === 'chat'){
        console.log('onmessage', event.data)
        setChatMessages(prev => [...prev, data]);
        setToScrollDown(true);
      }
      else if (data.type === 'online_status') {
        console.log(data, selectedChat.companion.id)
        if (data.sender === selectedChat.companion.id) {
          selectedChat.companion = {...selectedChat.companion, is_online: data.is_online, last_online: data.last_online}
          setCompanion(selectedChat.companion)
        }
      }
      else if (data.type === 'user_typing'){
        console.log(data)
        if (data.sender === selectedChat.companion.id){
          setIsCompanionTyping(data.typing);
        }
      }
      else if (data.type === 'mark_message_as_read'){
        setChatMessages(prev => [...prev.map(message => message.id===data.message_pk ? {...message, is_read: true}: {...message})])
      }
    }
    chatSocket.current.onclose = (event) => {
      setConnected(false);
      console.log('Socket clost');
    }
    chatSocket.current.onerror = (event) => {
      console.log('Socket error');
    }
  }

  const sendTypingStatus = async () => {
    if (connected){
      chatSocket.current.send(JSON.stringify({
        'typing': isTyping,
      }))
    }
  }

  const sendInputData = async () => {
    if(connected && (messageInput || fileInput)){
      chatSocket.current.send(JSON.stringify({
        'message': messageInput,
        'file': fileInput,
      }))
      setIsTyping(false);
      setMessageInput('');
      setFileInput(null);
    }
  }
  const markMessageAsRead = async (message) => {
    if(connected){
      chatSocket.current.send(JSON.stringify({
        'mark_message_as_read': message.id,
      }))
    }
  }
  // todo: сохранять только при отправке сообщения
  const uploadMessageFile = async (event) => {
    console.log(event.target.files[0])
    let response = await api.post(`api/v1/message/file/upload/`, {
      'image': event.target.files[0]
    },
        {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
}
    );
    if (response.status === 201){
      return response.data;
    }
  }

  const handlePhotoChange = event => {
    console.log(event.target.files[0])
    uploadMessageFile(event).then(data => {setFileInput(data['id'])})

  };


  useEffect(() => {
    if (selectedChat){
      // console.log('ФЕТЧИМ ЧАТ ID И СОЗДАЕМ WS');
      // fetchChatId().then(chat_id => loadWebSocket(chat_id));
      setCompanion(selectedChat.companion)
      loadWebSocket(selectedChat.id)
      console.log('ФЕТЧИМ СООБЩЕНИЯ', selectedChat);
      fetchMessages().then(messages => setChatMessages(messages));
    }
  }, [selectedChat]);


  useEffect(() => {
    if(chatMessages.length){
      addUnreadTitle('.messages', 'li.unread')
      scrollToElement('.messages', 'li.unread');

    }
  }, [connected]);

  useEffect(() => {
    if (toScrollDown){
      scrollDown('.messages', true);
      setToScrollDown(false);
    }
  }, [toScrollDown]);

  useEffect(() => {
    sendTypingStatus();
  }, [isTyping])

  function updateTimeout(){
    if (timerId) {
      clearTimeout(timerId);
    }
    let timer = setTimeout(() => {
      setIsTyping(false);
    }, 2000)
    setTimerId(timer);

  }


  if (selectedChat && connected){
    return(
      <>
        <div className="room-header black-light-bg mx-1 d-flex flex-row align-items-center px-5">
          <img
            src={
              companion.profile_image.indexOf('http') === -1
                ? 'http://127.0.0.1:8000' + companion.profile_image
                : companion.profile_image
            }
            alt=""
            className="img-fluid rounded-circle"
            style={{ height: '4rem', width: '4rem' }}
          />
          <div className="mx-3">
            <h1 className="p-0 m-0">{companion.username}</h1>
            <div><small>{isCompanionTyping ? 'Печатает...' : (companion.is_online ? 'Онлайн' : `Был онлайн ${TimestampToTimezone(companion.last_online).toFormat('yyyy-MM-dd в HH:mm')}`)}</small></div>
          </div>
        </div>

        <div className="messages flex-grow-1 overflow-auto mb-3 px-5">
          <ul className="message-list list-unstyled d-flex flex-column gap-2 my-3 px-5">
            {chatMessages.map((message, index) => (
                <>
                  <ChatRoomMessage
                    key={message.id}
                    message={message}
                    onMessageRead={markMessageAsRead}
                    position={message.sender === user.user_id ? 'right': 'left'}
                  />
                </>
            ))}
          </ul>
        </div>

        <div className="container">
          <div id="message-form" className="input-group input-group-lg mx-auto mb-3 justify-content-end w-50" >
            <div>
              <label
                  onChange={handlePhotoChange}
                  htmlFor="image"
              >
                <input type="file" accept="image/*" placeholder="Фото" name="profile_photo" id="image" hidden/>
                <MdOutlineAddAPhoto size="3rem"/>
              </label>
            </div>
            <input
              id="message-input"
              type="text"
              className="form-control shadow-none border-dark black-light-bg rounded-pill rounded-end"
              placeholder="Cообщение..."
              value={messageInput}
              onChange={event => {setMessageInput(event.target.value); setIsTyping(true); updateTimeout(); console.log('typing...')}}
              onBlur={event => {setIsTyping(false); console.log('not typing')}}
              onKeyDown={(event) => {event.key === 'Enter' && sendInputData()}}
              >
            </input>
            <button onClick={sendInputData} className="btn purple-bg rounded-pill rounded-start align-self-center"><VscSend size="1.75rem"/></button>
          </div>
        </div>
      </>
    )
  }
  else{
    return (
      <>
      </>
      )
  }
}

export default PageChats;