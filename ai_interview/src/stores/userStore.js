import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
    state(){
        return {
            user: {
                id: "",
                email: "",
                password: "",
                join_time: ""
            },
        }
    },
    actions: {
        setUser(user) {
            this.user = user;
        } 
    }
})