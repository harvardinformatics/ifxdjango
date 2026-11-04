import moment from 'moment'

export function useFilters() {
  const users = (value) => {
    let names = []
    if (value) {
      if (Array.isArray(value)) {
        names = value.map((u) => {
          return u.full_name ? u.full_name : u.username
        })
      } else {
        names = [value.full_name ? value.full_name : value.username]
      }
    }
    return names.join(', ')
  }

  const yesno = (value) => {
    return value ? 'Yes' : 'No'
  }

  const humanDate = (value) => {
    let datestr = ''
    if (value) {
      datestr = moment(String(value)).format('M/DD/YYYY')
    }
    return datestr
  }

  const humanDatetime = (value) => {
    let datestr = ''
    if (value) {
      datestr = moment(String(value)).format('M/DD/YYYY h:mm A')
    }
    return datestr
  }

  const timeOnly = (value) => {
    let datestr = ''
    if (value) {
      datestr = moment(String(value)).format('h:mm A')
    }
    return datestr
  }

  const spelledOutDay = (value) => {
    let datestr = ''
    if (value) {
      datestr = moment(String(value)).format('dddd, MMMM Do')
    }
    return datestr
  }

  const stateDisplay = (value) => {
    if (!value) return ''
    return value.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase())
  }

  return {
    users,
    yesno,
    humanDate,
    humanDatetime,
    timeOnly,
    spelledOutDay,
    stateDisplay
  }
}

export default useFilters
