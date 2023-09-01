import React, {useEffect, useRef} from 'react';
import { useInView } from 'react-intersection-observer';
import timestampToTimezone from "../../utils/timestampToTimezone.js";
import {BiCheckDouble, BiCheck} from "react-icons/bi";


function ChatRoomMessage({ message, onMessageRead, position }) {
  const listItemRef = useRef();
  const [inViewRef, inView] = useInView();

  const sendingTimezone = timestampToTimezone(message.sending_timestamp)

  useEffect(() => {
    if (position === 'left' && inView && !message.is_read){
      onMessageRead(message);
    }
  }, [inView])


  return (
    <>
      {position === 'right' ?
        <li
          id={message.id}
          ref={listItemRef}
          className={`message-right px-3 align-self-end w-65 ${message.is_read ? 'read' : ''} ${inView ? 'visible' : ''}`}
        >
          <div ref={inViewRef} className="d-flex justify-content-end">
            <div className="rounded-3 p-2 purple-message text-start" style={{wordBreak: 'break-word'}}>
              {message.text}
              <div className="d-flex justify-content-end align-items-center">
                <small className="message-time custom-text-muted">
                  {sendingTimezone.toFormat('HH:mm')}
                </small>
                {message.is_read ? <BiCheckDouble/> : <BiCheck/>}
              </div>
            </div>
          </div>
        </li>
              :
        <li
           id={message.id}
           ref={listItemRef}
           className={`message-left px-3 align-self-start w-65 ${message.is_read ? 'read' : 'unread'} ${inView ? 'visible' : ''}`}
        >
          <div ref={inViewRef} className='d-flex justify-content-start'>
            <div className="rounded-3 p-2 black-message text-start" style={{wordBreak: 'break-word'}}>{message.text}
              <div className="align-self-end">
                <small className="message-time d-flex justify-content-end">
                  {sendingTimezone.toFormat('HH:mm')}
                </small>
              </div>
            </div>
          </div>
        </li>
      }
    </>
  );
}

export default ChatRoomMessage;
