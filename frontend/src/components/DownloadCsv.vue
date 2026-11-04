<template>
  <span @click="exportCsv" style="cursor: pointer">
    <slot></slot>
  </span>
</template>

<script>
export default {
  name: 'DownloadCsv',
  props: {
    data: {
      type: Array,
      required: true,
    },
    labels: {
      type: Object,
      default: () => ({}),
    },
    name: {
      type: String,
      default: 'data.csv',
    },
    delimiter: {
      type: String,
      default: ',',
    },
  },
  methods: {
    exportCsv() {
      if (!this.data || this.data.length === 0) {
        return
      }

      const keys = Object.keys(this.data[0])
      const headers = keys.map((key) => this.labels[key] || key)

      const csvRows = []
      csvRows.push(headers.map((h) => this.escapeCsvValue(h)).join(this.delimiter))

      for (const row of this.data) {
        const values = keys.map((key) => {
          const val = row[key]
          return this.escapeCsvValue(val)
        })
        csvRows.push(values.join(this.delimiter))
      }

      const csvContent = csvRows.join('\n')
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const url = URL.createObjectURL(blob)

      const link = document.createElement('a')
      link.setAttribute('href', url)
      link.setAttribute('download', this.name.endsWith('.csv') ? this.name : `${this.name}.csv`)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    },
    escapeCsvValue(val) {
      if (val === null || val === undefined) {
        return ''
      }
      const str = String(val)
      if (str.includes(this.delimiter) || str.includes('"') || str.includes('\n')) {
        return `"${str.replace(/"/g, '""')}"`
      }
      return str
    },
  },
}
</script>
