// clipboardHelper.js
export function copyToClipboard(value, messageInstance) {
  if (navigator.clipboard && window.isSecureContext) {
    // 如果浏览器支持 navigator.clipboard 并且处于安全上下文（HTTPS），使用新的 API
    navigator.clipboard.writeText(value)
      .then(() => {
        messageInstance.success("复制成功");
      })
      .catch(() => {
        messageInstance.error("复制失败");
      });
  } else {
    // 如果不支持 navigator.clipboard 或不在安全上下文中，使用传统的复制方法
    const textarea = document.createElement('textarea');
    textarea.value = value;
    textarea.style.position = 'fixed';  // 防止在页面上显示
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try {
      const successful = document.execCommand('copy');
      if (successful) {
        messageInstance.success("复制成功");
      } else {
        messageInstance.error("复制失败");
      }
    } catch (err) {
      messageInstance.error("复制失败");
    }
    document.body.removeChild(textarea);
  }
}