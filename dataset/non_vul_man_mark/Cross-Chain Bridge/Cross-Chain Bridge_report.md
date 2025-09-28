# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokensDeposited1, TokensReleased2
- **rel_chain**: RoleGranted, RoleRevoked, Upgraded, Transfer, Approval
- **det_chain**: TokensReleased1, BoughtBackAndBurned2
### src_chain: Ethereum
- **事件**: TokensDeposited1
  - 函数: depositERC20
  - 关键操作: require(amount > 0, 'CrossChainBridgeERC20: amount cannot be 0'), require(receiverAddress != address(0), 'CrossChainBridgeERC20: invalid receiverAddress provided'), require(address(token) != address(0), 'CrossChainBridgeERC20: invalid token address provided')
- **事件**: TokensReleased2
  - 函数: _releaseERC20
  - 关键操作: require(!releasedDeposits[depositChainId][depositNumber], 'CrossChainBridgeERC20: Deposit was already processed and released'), require(receiverAddress != address(0), 'CrossChainBridgeERC20: invalid receiverAddress provided'), require(sourceNetworkTokenAddress != address(0), 'CrossChainBridgeERC20: invalid sourceNetworkTokenAddress provided'), require(token.balanceOf(address(this)) >= amount, 'CrossChainBridgeERC20: Not enough liquidity in bridge')
### rel_chain: RelayChain
- **事件**: RoleGranted
  - 函数: grantRole
  - 关键操作: require(hasRole(getRoleAdmin(role), _msgSender()), 'AccessControl: account is missing role'), _grantRole(role, account)
- **事件**: RoleRevoked
  - 函数: revokeRole
  - 关键操作: require(hasRole(getRoleAdmin(role), _msgSender()), 'AccessControl: account is missing role'), _revokeRole(role, account)
- **事件**: Upgraded
  - 函数: _upgradeTo
  - 关键操作: StorageSlot.getAddressSlot(_IMPLEMENTATION_SLOT).value = newImplementation;, emit Upgraded(newImplementation)
- **事件**: Transfer
  - 函数: transfer
  - 关键操作: require(recipient != address(0), 'ERC20: transfer to the zero address'), uint256 senderBalance = _balances[sender]; require(senderBalance >= amount, 'ERC20: transfer amount exceeds balance')
- **事件**: Approval
  - 函数: approve
  - 关键操作: require(spender != address(0), 'ERC20: approve to the zero address'), _allowances[owner][spender] = amount; emit Approval(owner, spender, amount)
### det_chain: Ethereum
- **事件**: TokensReleased1
  - 函数: releaseERC20
- **事件**: BoughtBackAndBurned2
  - 函数: buyBackAndBurnERC20
  - 关键操作: require(collectedToken != address(0), 'BuyBackAndBurnV1: invalid token address'), uint256 amount = collectedERC20ToBurn[collectedToken], ERC20Burnable(address(burnToken)).burn(balanceBurnToken)
---
