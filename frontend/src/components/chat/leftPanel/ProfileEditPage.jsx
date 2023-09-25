import React, {useContext, useState, useEffect} from 'react'
import useAxios from '../../../utils/useAxios'
import AuthContext from '../../../context/AuthContext'
import {MdOutlineAddAPhoto} from 'react-icons/md'


function ProfileEditPage({setActivePanel}) {
  const api = useAxios()
  const {user} = useContext(AuthContext)
  const [profile, setProfile] = useState(null)
  const [newPhotoUploaded, setNewPhotoUploaded] = useState(false)
  const [formData, setFormData] = useState({})
  const [formError, setFormError] = useState('')

  async function fetchProfile() {
    let response = await api.get(`api/v1/profile/${user.user_id}/`)
    if (response.status === 200){
      return response.data
    }
  }

  const handleChange = event => {
      const { name, value } = event.target
      setFormData({
          ...formData,
          [name]: value,
      })
  }

  const handlePhotoChange = event => {
    console.log(event.target.files[0])

    setFormData({
        ...formData,
        profile_image: event.target.files[0],
    })
    setNewPhotoUploaded(true)
  }
  const handleSubmit = event => {
    event.preventDefault()
    const formDataToSend = new FormData()
    for (const key in formData) {
        if (formData[key] !== profile[key]){
          formDataToSend.append(key, formData[key])
        }
    }

    api.patch(`/api/v1/user/${user.user_id}/`, formDataToSend)
      .then(response => {
        setActivePanel('profile')
      })
      .catch(error => {
        setFormError(error.toString())
      })
  }


  useEffect(() => {
    fetchProfile().then(response => {
      setProfile(response)
      setFormData(response)
    })
    
  }, [])


  if (formData) {
    return (
        <div className="form-group m-3">
          {formError && <div>{formError}</div>}
            <form onSubmit={handleSubmit}>
                <div>
                  {(formData.profile_image ||newPhotoUploaded ) &&
                    <img
                      src={newPhotoUploaded ?
                            URL.createObjectURL(formData.profile_image)
                                :
                            (profile.profile_image.indexOf('http') === -1 ?
                                'http://127.0.0.1:8000' + profile.profile_image
                                : profile.profile_image
                            )
                      }
                      className="img-fluid mh-100 w-auto p-3 pb-1" alt=""
                    />
                  }
                </div>
                <div>
                  <label onChange={handlePhotoChange} htmlFor="image">
                    <input type="file" accept="image/*" placeholder="Фото" name="profile_photo" id="image" hidden/>
                    <MdOutlineAddAPhoto size="3rem"/>
                  </label>
                </div>
                <input className="form-control my-1" type="text" placeholder="Имя" name="first_name" value={formData.first_name || ''} onChange={handleChange} />
                <input className="form-control my-1" type="text" placeholder="Фамилия" name="last_name" value={formData.last_name || ''} onChange={handleChange} />
                <input className="form-control my-1" type="text" placeholder="Биография" name="bio" value={formData.bio || ''} onChange={handleChange} />
                <button className="btn purple-bg mx-3 my-1" type="submit">Сохранить изменения</button>
            </form>
        </div>
    )
  }
  else {
    return (
        <>
        </>
    )
  }
}

export default ProfileEditPage