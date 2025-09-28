# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: NewProviderOffer1, AddLiquidity1, RemoveLiquidity1
- **rel_chain**: Swap, SwappedOneProvider
- **det_chain**: AddLiquidity1, RemoveLiquidity1, Swap1
### src_chain: source_chain
- **事件**: NewProviderOffer1
  - 函数: createOrder
  - 关键操作: require(IOSWAP_RestrictedFactory(factory).isLive(), 'GLOBALLY PAUSED'), require(isLive, 'PAUSED'), require(msg.sender == restrictedLiquidityProvider || msg.sender == provider, 'Not from router or owner'), require(expire >= startDate, 'Already expired'), require(expire >= block.timestamp, 'Already expired')
- **事件**: AddLiquidity1
  - 函数: addLiquidity
  - 关键操作: require(IOSWAP_RestrictedFactory(factory).isLive(), 'GLOBALLY PAUSED'), require(isLive, 'PAUSED'), require(msg.sender == restrictedLiquidityProvider || msg.sender == offer.provider, 'Not from router or owner'), require(!offer.locked, 'Offer locked')
- **事件**: RemoveLiquidity1
  - 函数: removeLiquidity
  - 关键操作: require(msg.sender == restrictedLiquidityProvider || msg.sender == provider, 'Not from router or owner'), require(offer.locked || offer.expire < block.timestamp, 'Offer not expired')
### rel_chain: relay_chain
- **事件**: Swap
  - 函数: swap
  - 关键操作: require(isLive, 'PAUSED'), require(amount0Out == 0 && amount1Out != 0 || amount0Out != 0 && amount1Out == 0, 'Not supported'), require(amount0Out < _reserve0 && amount1Out < _reserve1, 'INSUFFICIENT_LIQUIDITY')
- **事件**: SwappedOneProvider
  - 函数: removeLiquidity
  - 关键操作: require(msg.sender == oracleLiquidityProvider || msg.sender == provider, 'Not from router or owner'), require(expire > block.timestamp, 'Already expired'), offer.amount = offer.amount.sub(amountOut), offer.reserve = offer.reserve.sub(reserveOut)
### det_chain: destination_chain
- **事件**: AddLiquidity1
  - 函数: addLiquidity
  - 关键操作: require(IOSWAP_RestrictedFactory(factory).isLive(), 'GLOBALLY PAUSED'), require(isLive, 'PAUSED'), require(msg.sender == restrictedLiquidityProvider || msg.sender == offer.provider, 'Not from router or owner'), require(amountIn > 0, 'No amount in')
- **事件**: RemoveLiquidity1
  - 函数: removeLiquidity
  - 关键操作: require(msg.sender == restrictedLiquidityProvider || msg.sender == provider, 'Not from router or owner'), require(offer.locked || offer.expire < block.timestamp, 'Offer not expired')
- **事件**: Swap1
  - 函数: swap
  - 关键操作: require(tx.origin == msg.sender && !Address.isContract(msg.sender) && trader == msg.sender, 'Invalid trader'), require(isLive, 'PAUSED'), require(offer.allowAll || isApprovedTrader[direction][offerIdx][trader], 'Not a approved trader'), require(block.timestamp >= offer.startDate, 'Offer not begin yet'), require(block.timestamp <= offer.expire, 'Offer expired')
---
