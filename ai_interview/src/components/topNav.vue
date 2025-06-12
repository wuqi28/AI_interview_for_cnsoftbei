<template>
    <t-head-menu v-model="menu1Value" theme="light" @change="changeHandler" style="width: 100%;">
        <template #logo>
            <img height="28" src="../../public/img/logo_chinese.png" alt="logo" />
        </template>
        <template #operations>
            <router-link to="/">
                <t-tooltip class="placement align" content="点击回到主页" :overlay-style="{ width: '200px' }"
                    placement="left" show-arrow>
                    <t-button variant="text" shape="square">
                        <template #icon><t-icon name="login" /></template>
                    </t-button>
                </t-tooltip>
            </router-link>
        </template>
    </t-head-menu>
</template>

<script setup>
import { ref } from 'vue';

// 当前选中的菜单项的值
const menu1Value = ref('item1');

// 菜单选择变化时的处理函数
const changeHandler = (value) => {
    console.log('当前选中的菜单项值为:', value);
};
</script>

<style scoped>
/* 可以在这里添加自定义样式 */
</style>
