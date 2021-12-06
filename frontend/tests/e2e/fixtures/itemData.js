import FT from './fieldTypes'

export default [
   {
     type: 'user',
     title: 'Users',
     url: 'users',
     searchText: 'a',
     listLength: 5,
     canDeleteFromDetail: true,
     inputs: {
       create: [
         {
           key: '',
           value: 0,
           type: ''
         }
       ],
       update: [
         {
           key: '',
           value: 0,
           type: ''
         }
       ]
     }
   },
  {
    type: 'organization',
    title: 'Organizations',
    url: 'organizations',
    searchText: 'b',
    searchItem: 'My Cool School',
    listLength: 6,
    canDeleteFromDetail: true,
    inputs: {
      create: [
        {
          key: 'name',
          value: 'My Cool School',
          type: FT.TEXT,
        },
        {
          key: 'rank',
          value: 'School',
          type: FT.SELECT,
        },
        {
          key: 'org-tree',
          value: 'Local',
          type: FT.TEXT,
        },
      ],
      update: [
        {
          key: 'name',
          value: 'UPDATE',
          type: FT.TEXT,
        },
      ],
    },
  },
  {
    type: 'message',
    title: 'Messages',
    url: 'messages',
    searchText: 'cns',
    searchItem: 'Important Message',
    listLength: 3,
    canDeleteFromDetail: false,
    inputs: {
      create: [
        {
          key: 'name',
          value: 'Important Message',
          type: FT.TEXT,
        },
        {
          key: 'subject',
          value: 'An Important Message',
          type: FT.TEXT,
        },
        {
          key: 'message',
          value: 'This is an important message.',
          type: FT.TEXT,
        },
      ],
      update: [
        {
          key: 'message',
          value: " It's <b>super</b> important",
          type: FT.TEXT,
        },
      ],
    },
  },
]
