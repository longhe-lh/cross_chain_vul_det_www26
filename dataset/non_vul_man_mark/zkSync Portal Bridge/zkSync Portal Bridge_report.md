# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: depositERC201, withdrawPendingBalance1
- **rel_chain**: proveBlocks
- **det_chain**: finalizeDeposit1, withdraw1
### src_chain: L1
- **事件**: depositERC201
  - 函数: depositERC20
  - 关键操作: require(_zkSyncAddress != SPECIAL_ACCOUNT_ADDRESS, "P");, requireActive();, registerDeposit(tokenId, depositAmount, _zkSyncAddress);
- **事件**: withdrawPendingBalance1
  - 函数: withdrawPendingBalance
  - 关键操作: uint16 tokenId = 0;, if (_token != address(0)) { tokenId = governance.validateTokenAddress(_token); }, bytes22 packedBalanceKey = packAddressAndTokenId(_owner, tokenId);, uint128 balance = pendingBalances[packedBalanceKey].balanceToWithdraw;, uint128 amount = Utils.minU128(balance, _amount);, require(amount > 0, "f1");, if (tokenId == 0) { ... } else { ... };, pendingBalances[packedBalanceKey].balanceToWithdraw = balance - amount;
### rel_chain: L2
- **事件**: proveBlocks
  - 函数: proveBlocks
  - 关键操作: requireActive();, governance.requireActiveValidator(msg.sender);, for (uint32 i = 0; i < _newBlocksData.length; ++i) { ... }, require(success, "p");
### det_chain: L1
- **事件**: finalizeDeposit1
  - 函数: finalizeDeposit
  - 关键操作: IERC20 l1Token = IERC20(l1TokenAddress);, l1Token.transferFrom(_l1Sender, address(this), _amount);, emit FinalizeDeposit(_l1Sender, _l2Receiver, _amount);
- **事件**: withdraw1
  - 函数: withdraw
  - 关键操作: IERC20 token = IERC20(l2TokenAddress);, token.transfer(_l1Receiver, _amount);, emit Withdrawal(_l1Receiver, _amount);
---
