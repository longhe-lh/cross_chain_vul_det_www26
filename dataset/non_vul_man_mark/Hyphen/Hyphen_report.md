# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenDepositAndSwap2
- **rel_chain**: depositErc20, depositNative, sendFundsToUser, swapAndSendFundsToUser
- **det_chain**: AssetSent1, DepositAndSwap2
### src_chain: source_chain
- **事件**: TokenDeposit1
  - 函数: depositErc20
  - 关键操作: require(tokenAddress != address(0), "Token address cannot be 0"), require(tokensInfo[tokenAddress].supportedToken, "Token not supported"), SafeERC20Upgradeable.safeTransferFrom(IERC20Upgradeable(tokenAddress), sender, address(this), amount)
- **事件**: TokenDepositAndSwap2
  - 函数: depositAndSwapErc20
  - 关键操作: require(tokenAddress != NATIVE, "wrong function"), require(receiver != address(0), "Receiver address cannot be 0")
### rel_chain: relay_chain
- **事件**: depositErc20
  - 函数: depositErc20
  - 关键操作: require(tokensInfo[tokenAddress].minCap <= amount && tokensInfo[tokenAddress].maxCap >= amount, "Deposit amount should be within allowed Cap limits"), emit Deposit(sender, tokenAddress, receiver, toChainId, amount)
- **事件**: depositNative
  - 函数: depositNative
  - 关键操作: require(tokensInfo[NATIVE].minCap <= msg.value && tokensInfo[NATIVE].maxCap >= msg.value, "Deposit amount not in Cap limit"), emit Deposit(_msgSender(), NATIVE, receiver, toChainId, msg.value + rewardAmount, rewardAmount, tag)
- **事件**: sendFundsToUser
  - 函数: sendFundsToUser
  - 关键操作: require(receiver != address(0), "Bad receiver address"), processedHash[hashSendTransaction] = true
- **事件**: swapAndSendFundsToUser
  - 函数: swapAndSendFundsToUser
  - 关键操作: require(swapRequests.length > 0, "Wrong method call"), require(swapAdaptorMap[swapAdaptor] != address(0), "Swap adaptor not found")
### det_chain: destination_chain
- **事件**: AssetSent1
  - 函数: sendFundsToUser
- **事件**: DepositAndSwap2
  - 函数: depositAndSwapErc20
---
