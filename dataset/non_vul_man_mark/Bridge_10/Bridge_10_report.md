# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: SwapInitialized1
- **det_chain**: RedeemInitialized1
### src_chain: source_chain
- **事件**: SwapInitialized1
  - 函数: swap
  - 关键操作: IExampleToken(erc20from).burn(msg.sender, amount), nonce += 1
### rel_chain: relay_chain
- 无事件
### det_chain: destination_chain
- **事件**: RedeemInitialized1
  - 函数: redeem
  - 关键操作: require(isERC20valid[chainIdfrom][erc20from], "Chain id or ERC20 address from is not valid"), require(isERC20valid[getChainID()][erc20to], "ERC20 on this chain is not valid"), require(checkSign(recepient, amount, chainIdfrom, erc20from, nonce, v, r, s), "Input is not valid"), redeemStatus[redeemHash] = Status.Undone, require(redeemStatus[redeemHash] == Status.Undone, "Hash is not valid"), redeemStatus[redeemHash] = Status.Done, IExampleToken(erc20to).mint(recepient, amount)
---
