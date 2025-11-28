/**
 * Prisma 客户端单例
 * 
 * @author seven
 * @since 2024
 */
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

/**
 * 获取 Prisma 客户端实例（单例模式）
 * 在开发环境中，每次代码变更会创建新实例，生产环境中复用实例
 * 
 * @return {PrismaClient} Prisma 客户端实例
 * @author seven
 * @since 2024
 */
export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}

/**
 * 初始化数据库
 * 创建必要的表结构（通过 Prisma migrate 管理）
 * 
 * @author seven
 * @since 2024
 */
export async function initDatabase(): Promise<void> {
  try {
    // Prisma 会在首次连接时自动创建表（如果使用 db push）
    // 或者通过 migrate dev 来管理迁移
    await prisma.$connect();
    console.log('数据库连接成功');
  } catch (error) {
    console.error('数据库初始化失败:', error);
    throw error;
  }
}

