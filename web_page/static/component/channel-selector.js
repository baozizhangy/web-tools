// components/channel-selector.js

export default {
  name: 'channel-selector',
  props: {
    modelValue: String
  },
  emits: ['update:modelValue', 'change'],
  data() {
    return {
      channelOptions: [
        { label: '乐享借', value: 'lxj' },
        { label: '挖财', value: 'wacai' }
      ]
    }
  },
  template: `
    <el-form-item label="选择授信渠道:">
      <el-select
        v-model="internalValue"
        placeholder="请选择授信渠道"
        clearable
        style="width: 100%;"
        @change="onChange">
        <el-option
          v-for="option in channelOptions"
          :key="option.value"
          :label="option.label"
          :value="option.value" />
      </el-select>
    </el-form-item>
  `,
  computed: {
    internalValue: {
      get() {
        return this.modelValue;
      },
      set(val) {
        this.$emit('update:modelValue', val);
      }
    }
  },
  methods: {
    onChange(val) {
      this.$emit('change', val);
    }
  }
}
