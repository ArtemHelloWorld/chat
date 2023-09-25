import { DateTime } from "luxon"


function timestampToTimezone(timestamp) {
  const userTimezone = DateTime.local().zoneName
  const utcDateTime = DateTime.fromMillis(timestamp).toUTC()
  const userDateTime = utcDateTime.setZone(userTimezone)
  return userDateTime
}

export default timestampToTimezone