import { defineStore } from "pinia"
import { useBaseStore } from "./StoreBase"

const requestStatusWaitTime = 1000 //ms
import axios from "axios"
export const useStatusStore = defineStore("status", {
  state: () => {
    return {
      lastStatusRequestTime: 0,

      lorRunning: false,
      localApiEnabled: false,
      localServer: null,
      localPlayerID: null,
    }
  },
  actions: {
    initAnalytics(uid) {
      if (window.ipcRenderer) {
        window.ipcRenderer.send("user-init", uid)
      }
    },
    processStatusInfo(data) {
      const baseStore = useBaseStore()

      if (data.playerId && this.localPlayerID != data.playerId) {
        // there is a new valid player ID
        this.initAnalytics(data.playerId)
      }

      if (data.language) {
        var newLocale = data.language.replace("-", "_").toLowerCase()
        if (baseStore.locale != newLocale) {
          console.log("Switch Locale", this.locale, newLocale)
          baseStore.changeLocale(newLocale)
        }
      }

      this.lorRunning = data.lorRunning
      this.localApiEnabled = data.isLocalApiEnable
      this.localServer = data.server
      this.localPlayerID = data.playerId
    },
    requestStatusInfo() {
      // Keeps requesting status
      const baseStore = useBaseStore()

      if (!baseStore.IS_ELECTRON) {
        // Skip for Web app
        return
      }

      this.lastStatusRequestTime = Date.now()
      axios
        .get(`${baseStore.apiBase}/status`)
        .then((response) => {
          this.processStatusInfo(response.data)
          var elapsedTime = Date.now() - this.lastStatusRequestTime // ms
          if (requestStatusWaitTime > elapsedTime) {
            setTimeout(this.requestStatusInfo, requestStatusWaitTime - elapsedTime)
          } else {
            setTimeout(this.requestStatusInfo, 100)
          }
        })
        .catch((e) => {
          if (axios.isCancel(e)) {
            console.log("Request cancelled")
          } else {
            console.log("error", e)
            var elapsedTime = Date.now() - this.lastStatusRequestTime // ms
            if (elapsedTime > requestStatusWaitTime) {
              setTimeout(this.requestStatusInfo, 100)
            } else {
              setTimeout(this.requestStatusInfo, requestStatusWaitTime - elapsedTime)
            }
          }
        })
    },
  },
})