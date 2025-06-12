import { defineStore } from 'pinia'

export const usePageStore = defineStore('page', {
    state(){
        return {
            pageIndex: "1",
        }
    },
    actions: {
        changePageIndex(pageIndex) {
            this.pageIndex = pageIndex;
        }
    }
})