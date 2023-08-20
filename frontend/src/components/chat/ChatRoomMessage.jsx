import React, {useEffect, useRef} from 'react';
import { useInView } from 'react-intersection-observer';
import timestampToTimezone from "../../utils/timestampToTimezone.js";
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
            <div className="rounded-3 p-2 bg-light text-black text-start" style={{wordBreak: 'break-word'}}>
              {message.text}
              <div className="align-self-end">
                <small className="message-time d-flex justify-content-end text-muted">
                  {sendingTimezone.toFormat('HH:mm')} {message.is_read ? 'read' : ''}
                </small>
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
            <div className="rounded-3 p-2 bg-secondary text-light text-start" style={{wordBreak: 'break-word'}}>{message.text}
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





//
//
// {message.sender === user.user_id ? (
//
//               ) : (
//                 <li className={`message-left px-3 align-self-start w-65`} id={message.id}>
//                   <div className={`d-flex justify-content-start ${true ? 'read' : ''}`}>
//                     <div className="rounded-3 p-2 bg-secondary text-light text-start" style={{wordBreak: 'break-word'}}>{message.text}
//                       <div className="align-self-end">
//                         <small className="message-time d-flex justify-content-end">
//                           {message.time_sending}
//                         </small>
//                       </div>
//                     </div>
//                   </div>
//                 </li>
//               )}