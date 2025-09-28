# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: mint, withdraw
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: SourceChain
- **事件**: TokenDeposit1
  - 函数: pledge
  - 关键操作: require(borERC20().allowance(msg.sender, address(this)) >= _amount);, borERC20().transferFrom(msg.sender, address(tunnel(_tunnelKey)), _amount);, tunnel(_tunnelKey).pledge(msg.sender, _amount);
- **事件**: TokenRedeem2
  - 函数: redeem
  - 关键操作: require(tunnel(_tunnelKey).canIssueAmount() > otoken(_tunnelKey).totalSupply(), 'Not enough pledge value');, tunnel(_tunnelKey).redeem(msg.sender, _amount);
### rel_chain: RelayChain
- **事件**: mint
  - 函数: approveMint
  - 关键操作: if (to == address(0)) { return; }, uint256 trusteeCount = getRoleMemberCount(_tunnelKey);, bool shouldMint = mintProposal().approve(...);, if (!shouldMint) { return; }, tunnel(_tunnelKey).issue(to, _amount);
- **事件**: withdraw
  - 函数: burnBToken
  - 关键操作: require(tunnel(_tunnelKey).canIssueAmount() > otoken(_tunnelKey).totalSupply(), 'Not enough pledge value');, tunnel(_tunnelKey).burn(msg.sender, amount, assetAddress);
### det_chain: DestinationChain
- **事件**: TokenWithdraw1
  - 函数: unlock
  - 关键操作: require(supportToken(token0, chainID) != address(0), 'Not Support Token');, IERC20Upgradeable(token0).safeTransfer(to, amount);
- **事件**: TokenMint2
  - 函数: lock
  - 关键操作: require(supportToken(token0, chainID) != address(0), 'Not Support Token');, IERC20Upgradeable(token0).safeTransferFrom(from, address(this), amount);, emit Lock(token0, supportToken(token0, chainID), chainID, from, to, amount);
---
