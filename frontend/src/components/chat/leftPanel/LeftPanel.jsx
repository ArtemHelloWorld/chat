import React, { useState, useContext } from 'react';
import ChatList from './ChatList';
import ProfilePage from './ProfilePage';
import ProfileEditPage from './ProfileEditPage';
import { Dropdown, DropdownButton} from 'react-bootstrap';
import {IoMdArrowBack} from 'react-icons/io'
import {MdModeEdit, MdMenu} from 'react-icons/md'
import AuthContext from '../../../context/AuthContext';
import UserSearchPage from './UserSearchPage';

const LeftPanel = ({selectedChat, setSelectedChat}) => {
  const [activePanel, setActivePanel] = useState('chat-list');
  const {logoutUser} = useContext(AuthContext)
  const [querySelectorValue, setQuerySelectorValue] = useState('');

  return (
      <>
        {activePanel === 'chat-list' &&
            <>
              <div className="d-flex justify-content-start px-3 pt-2">
                <DropdownButton id="dropdown-button e-caret-hide" variant='dark' className="black-light-bg" title={<MdMenu size="2rem" />}>
                  <Dropdown.Item onClick={() => setActivePanel('profile')}>Profile</Dropdown.Item>
                  <Dropdown.Item onClick={() => logoutUser()}>Logout</Dropdown.Item>
                </DropdownButton>
                <input
                    id="message-input"
                    type="text"
                    className="form-control shadow-none border-dark black-dark-bg rounded-pill"
                    placeholder="Поиск"
                    onClick={() => setActivePanel('user-search')}
                    >
                  </input>
              </div>
              <ChatList selectedChat={selectedChat} setSelectedChat={setSelectedChat}/>
            </>
        }

        {activePanel === 'user-search' &&
            <>
              <div className="d-flex justify-content-start px-3 pt-2">
                <IoMdArrowBack size="2rem" onClick={() => setActivePanel('chat-list')}/>
                <input
                    id="message-input"
                    type="text"
                    className="form-control shadow-none border-dark black-dark-bg rounded-pill"
                    placeholder="Поиск"
                    value={querySelectorValue}
                    onChange={event => {setQuerySelectorValue(event.target.value);}}
                    >
                  </input>
              </div>
              <UserSearchPage selectedChat={selectedChat} setSelectedChat={setSelectedChat} querySelectorValue={querySelectorValue}/>
            </>
        }

        {activePanel === 'profile' &&
            <>
              <div className="d-flex justify-content-between align-items-center mt-2 mx-3">
                  <IoMdArrowBack size="2rem" onClick={() => setActivePanel('chat-list')} />
                  <h2 className="panel-header mb-0" style={{ display: 'inline-block' }} >Profile</h2>
                  <MdModeEdit size="1.5rem" className="ml-auto" onClick={() => setActivePanel('edit-profile')} />
              </div>
              <ProfilePage/>
            </>
        }
        {
          activePanel === 'edit-profile' &&
            <>
              <div className="d-flex justify-content-start align-items-center px-3 pt-2">
                <IoMdArrowBack size="2rem" onClick={() => setActivePanel('profile')}/>
                <h2 className="panel-header mb-0" style={{ display: 'inline-block' }}>Edit Profile</h2>
              </div>
              <ProfileEditPage setActivePanel={setActivePanel}/>
            </>
        }
      </>
  );
}

export default LeftPanel;