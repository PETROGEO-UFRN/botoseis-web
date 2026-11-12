// *** The database client or an open transaction: helpers taking it run
// *** inside the caller's transaction when there is one
declare type IDatabaseExecutor =
  | typeof import('@/database/connection').database
  | import('@/database/connection').ITransaction
