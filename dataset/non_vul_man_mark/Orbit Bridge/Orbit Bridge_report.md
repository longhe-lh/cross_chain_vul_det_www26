# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Deposit1, DepositNFT2
- **rel_chain**: Withdraw, WithdrawNFT
- **det_chain**: Withdraw1, WithdrawNFT2
### src_chain: ETH
- **事件**: Deposit1
  - 函数: depositToken
  - 关键操作: require(isValidChain[getChainId(toChain)]), require(token != address(0)), require(amount > 0), TIERC20(token).transferFrom(msg.sender, address(this), amount), decimal = TIERC20(token).decimals(), require(decimal > 0)
- **事件**: DepositNFT2
  - 函数: _depositNFT
  - 关键操作: require(isValidChain[getChainId(toChain)]), require(token != address(0)), require(IERC721(token).ownerOf(tokenId) == msg.sender), require(!silentTokenList[token]), IERC721(token).transferFrom(msg.sender, address(this), tokenId), require(IERC721(token).ownerOf(tokenId) == address(this))
### rel_chain: RelayChain
- **事件**: Withdraw
  - 函数: withdraw
  - 关键操作: require(bytes32s.length == 2), require(uints.length == chainUintsLength[getChainId(fromChain)]), require(uints[1] <= 100), require(fromAddr.length == chainAddressLength[getChainId(fromChain)]), require(bytes32s[0] == sha256(abi.encodePacked(hubContract, chain, address(this)))), require(isValidChain[getChainId(fromChain)]), require(!isUsedWithdrawal[whash]), isUsedWithdrawal[whash] = true, validatorCount = _validate(whash, v, r, s), require(validatorCount >= required), IERC20(token).safeTransfer(destination, amount)
- **事件**: WithdrawNFT
  - 函数: withdrawNFT
  - 关键操作: require(bytes32s.length == 2), require(uints.length == chainUintsLength[getChainId(fromChain)]), require(fromAddr.length == chainAddressLength[getChainId(fromChain)]), require(bytes32s[0] == sha256(abi.encodePacked(hubContract, chain, address(this)))), require(isValidChain[getChainId(fromChain)]), require(!isUsedWithdrawal[whash]), isUsedWithdrawal[whash] = true, validatorCount = _validate(whash, v, r, s), require(validatorCount >= required), IERC721(token).transferFrom(address(this), toAddr, uints[1])
### det_chain: OtherChain
- **事件**: Withdraw1
  - 函数: withdraw
  - 关键操作: require(bytes32s.length >= 1), require(bytes32s[0] == sha256(abi.encodePacked(hubContract, chain, address(this)))), require(uints.length >= 2), require(isValidChain[getChainId(fromChain)]), require(!isUsedWithdrawal[whash]), isUsedWithdrawal[whash] = true, validatorCount = _validate(whash, v, r, s), require(validatorCount >= required), TIERC20(tokenAddress).transfer(_toAddr, uints[0])
- **事件**: WithdrawNFT2
  - 函数: withdrawNFT
  - 关键操作: require(bytes32s.length >= 1), require(bytes32s[0] == sha256(abi.encodePacked(hubContract, chain, address(this)))), require(uints.length >= 2), require(isValidChain[getChainId(fromChain)]), require(!isUsedWithdrawal[whash]), isUsedWithdrawal[whash] = true, validatorCount = _validate(whash, v, r, s), require(validatorCount >= required), IERC721(token).transferFrom(address(this), toAddr, uints[1])
---
