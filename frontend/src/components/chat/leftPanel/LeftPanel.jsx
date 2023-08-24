import React, { useState, useContext } from 'react';
import ChatList from "../ChatList";
import ProfilePage from "./ProfilePage";
import ProfileEditPage from "./ProfileEditPage";
import { Dropdown, DropdownButton} from 'react-bootstrap';
import {IoMdArrowBack} from 'react-icons/io'
import {MdModeEdit, MdMenu} from 'react-icons/md'
import AuthContext from "../../../context/AuthContext";

const LeftPanel = ({setSelectedChat}) => {
  const [activePanel, setActivePanel] = useState('chat-list');
  const {logoutUser} = useContext(AuthContext)


  return (
      <>
        {activePanel === 'chat-list' &&
            <>
              <div className="d-flex justify-content-start px-3 pt-2">
                <DropdownButton id="dropdown-button e-caret-hide" variant='dark' title={<MdMenu size="2rem" />}>
                  <Dropdown.Item onClick={() => setActivePanel('profile')}>Profile</Dropdown.Item>
                  <Dropdown.Item onClick={() => logoutUser()}>Logout</Dropdown.Item>
                </DropdownButton>
              </div>
              <ChatList setSelectedChat={setSelectedChat}/>
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