import React, { useEffect, useState} from 'react'
import useAxios from '../../../utils/useAxios';

export default function UserSearchPage({ selectedChat, setSelectedChat, querySelectorValue }){
  const [users, setUsers] = useState([]);
  const api = useAxios();


  async function fetchChats(querySelectorValue) {
    let response = await api.get(`api/v1/user/search/${querySelectorValue}/`);
    if (response.status === 200){
      console.log(response.data);
      return response.data
    }
  }

  useEffect(() => {
      if (querySelectorValue.length) {
        fetchChats(querySelectorValue).then(
            data => {setUsers(data)}
        )
      }
      else {
        setUsers([])
      }
  }, [querySelectorValue]);

  async function handleUserClick(user) {
    let response = await api.get(`api/v1/chat/user/${user.username}/`);
    if (response.status === 200){
      setSelectedChat(response.data);
    }
  }

  if(users) {
    return (
        <div className="overflow-auto">
          <ul id="users" className="list-group overflow-auto my-3">
            {users.map((user) => (
              <li key={user.id} onClick={() => handleUserClick(user)}  className='mb-1 overflow-hidden' style={{ listStyle: 'none' }}>
                <a href={`#${user.username}`} className={`card text-decoration-none d-block border-2 h-100 p-0`}>
                  <div className="row align-items-start mw-100 h-100">
                    <div className="col-md-4">
                      <div className="card-img-square">
                        {user.profile_image && (
                          <img
                            src={
                              user.profile_image.indexOf('http') === -1
                                ? 'http://127.0.0.1:8000' + user.profile_image
                                : user.profile_image
                            }
                            alt=""
                            className="img-fluid rounded-circle"
                            style={{ height: '4rem', width: '4rem' }}
                          />
                          )
                        }
                      </div>
                    </div>
                    <div className="col-md-8 d-flex">
                      <div className="d-flex flex-column">
                        <div className="d-flex justify-content-between">
                          <div className="d-flex justify-content-start user-description text-truncate align-self-start mw-100">
                            <h4 className="user-username text-truncate align-self-start">{user.username}</h4>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </a>
              </li>
            ))}
          </ul>
        </div>
    );
  }
  else{
    return (
        <></>
    )
  }
}