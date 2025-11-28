/**
 * 启动 Polling 模式的脚本
 * 用于本地开发，不需要设置 Webhook
 * 
 * 使用方法：
 * 运行: npm run bot:dev
 * 
 * 如果遇到网络连接问题（ETIMEDOUT），可以在 .env 文件中配置代理：
 * PROXY_URL=http://proxy.example.com:8080
 * 
 * @author seven
 * @since 2024
 */
import '../lib/config'; // 确保环境变量加载
import { startPolling } from '../pages/api/polling';

// 启动 polling
startPolling().catch((error) => {
  console.error('启动失败:', error);
  if (error instanceof Error && error.message.includes('ETIMEDOUT')) {
    console.error('');
    console.error('========================================');
    console.error('网络连接超时错误！');
    console.error('========================================');
    console.error('可能的原因：');
    console.error('1. 网络无法访问 Telegram API（可能被防火墙阻止）');
    console.error('2. 需要配置代理');
    console.error('');
    console.error('解决方案：');
    console.error('1. 检查网络连接');
    console.error('2. 在 .env 文件中添加代理配置：');
    console.error('   PROXY_URL=http://your-proxy:port');
    console.error('3. 或者使用 VPN/代理工具');
    console.error('========================================');
  }
  process.exit(1);
});

// 优雅关闭
process.on('SIGINT', () => {
  console.log('收到停止信号，正在关闭...');
  process.exit(0);
});
