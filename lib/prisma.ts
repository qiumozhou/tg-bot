/**
 * Prisma 客户端单例（适配 Cloudflare D1）
 * 
 * @author seven
 * @since 2025-11-28
 */
import { PrismaClient } from '@prisma/client';
import { PrismaD1 } from '@prisma/adapter-d1';

// 全局类型定义，支持 D1 数据库绑定
declare global {
  var prisma: PrismaClient | undefined;
  var d1Database: D1Database | undefined;
}

/**
 * Prisma 客户端实例（单例）
 * 在 Cloudflare Workers 环境中使用 D1 Adapter
 * 在本地开发环境中使用标准 SQLite 连接
 */
export let prisma: PrismaClient | any;

/**
 * 初始化数据库连接
 * 
 * @param {D1Database} d1 - Cloudflare D1 数据库实例（仅在 Workers 环境中需要）
 * @return {Promise<void>}
 * @author seven
 * @since 2025-11-28
 */
export async function initDatabase(d1?: D1Database): Promise<void> {
  try {
    // 如果已经初始化过，直接返回
    if (global.prisma) {
      prisma = global.prisma;
      console.log('使用已存在的数据库连接');
      return;
    }
    
    console.log('初始化数据库连接...');
    
    // 在 Cloudflare Workers 环境中，使用 D1 Adapter
    if (d1) {
      console.log('检测到 D1 数据库绑定，使用 D1 Adapter');
      global.d1Database = d1;
      
      const adapter = new PrismaD1(d1);
      // @ts-ignore - PrismaClient with adapter type compatibility
      prisma = new PrismaClient({
        // @ts-ignore
        adapter,
        log: ['error', 'warn'],
      });
    }
    // 本地开发环境，使用标准 SQLite 连接
    else {
      console.log('本地开发环境，使用标准 SQLite 连接');
      prisma = new PrismaClient({
        log: process.env.NODE_ENV === 'development' 
          ? ['query', 'error', 'warn'] 
          : ['error'],
      });
    }
    
    // 缓存实例
    global.prisma = prisma;
    
    // 测试数据库连接
    await prisma.$connect();
    console.log('数据库连接成功');
  } catch (error) {
    console.error('数据库初始化失败:', error);
    throw error;
  }
}

/**
 * 关闭数据库连接
 * 
 * @author seven
 * @since 2025-11-28
 */
export async function disconnectDatabase(): Promise<void> {
  try {
    if (prisma) {
      await prisma.$disconnect();
      console.log('数据库连接已关闭');
    }
  } catch (error) {
    console.error('关闭数据库连接失败:', error);
  }
}

