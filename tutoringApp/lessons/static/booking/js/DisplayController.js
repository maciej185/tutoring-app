class DisplayController {
    constructor() {
        this.profileSelect = document.querySelector("select#sessions-filter-profile")
        this.dateInputFrom = document.querySelector("input#sessions-filter-from")
        this.dateInputTo = document.querySelector("input#sessions-filter-to")

        this.profileSelect.addEventListener("input", this.profileSelectSelectEventListener.bind(this))
        this.dateInputFrom.addEventListener("input", this.dateInputFromInputEventListener.bind(this))
        this.dateInputTo.addEventListener("input", this.dateInputToInputEventListener.bind(this))

        this.filterBtn = document.querySelector("div#sessions-filters-btn_filter")
        this.clearBtn = document.querySelector("div#sessions-filters-btn_clear")
        this.filterLink = document.querySelector("a#sessions-filters-btn_filter-link")

        this.currentUrl = window.location.href

        this.urlQueryParams = new URLSearchParams(window.location.search);

        this.setInitialInputValues()

        Array.from(this.urlQueryParams).length

        this.setFilterBtnDisplay = () => this.filterBtn.style.display = Array.from(this.urlQueryParams).length == 0 ? "none" : "block"
        this.clearBtn.style.display = Array.from(this.urlQueryParams).length == 0 ? "none" : "block"
    }

    profileSelectSelectEventListener(e) {
        const profile = e.currentTarget.value
        if (profile) {
            this.urlQueryParams.set("profile", profile)
        } else {
            this.urlQueryParams.delete("profile")
        }
        this.filterLink.setAttribute("href", `?${this.urlQueryParams.toString()}`)

        this.setFilterBtnDisplay()
    }

    dateInputFromInputEventListener(e) {
        const from = e.currentTarget.value
        if (from) {
            this.urlQueryParams.set("from", from)
        } else {
            this.urlQueryParams.delete("from")
        }
        this.filterLink.setAttribute("href", `?${this.urlQueryParams.toString()}`)

        this.setFilterBtnDisplay()
    }

    dateInputToInputEventListener(e) {
        const to = e.currentTarget.value
        if (to) {
            this.urlQueryParams.set("to", to)
        } else {
            this.urlQueryParams.delete("to")
        }
        this.filterLink.setAttribute("href", `?${this.urlQueryParams.toString()}`)

        this.setFilterBtnDisplay()
    }

    setInitialInputValues() {
        if (this.urlQueryParams.get("profile")) this.profileSelect.value = this.urlQueryParams.get("profile")
        if (this.urlQueryParams.get("to")) this.dateInputTo.value = this.urlQueryParams.get("to")
        if (this.urlQueryParams.get("from")) this.dateInputFrom.value = this.urlQueryParams.get("from")
    }

}

const display_controller = new DisplayController()