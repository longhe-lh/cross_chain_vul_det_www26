# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Cross1
- **rel_chain**: Voted, Executed
- **det_chain**: Claimed1
### src_chain: source_chain
- **事件**: Cross1
  - 函数: receiveTokensTo
  - 关键操作: IERC20(tokenToUse).safeTransferFrom(sender, address(this), amount), knownTokens[tokenToUse] = true, uint256 fee = amount.mul(feePercentage).div(feePercentageDivider), allowTokens.updateTokenTransfer(tokenToUse, formattedAmount)
  - 函数: depositTo
  - 关键操作: require(address(wrappedCurrency) != NULL_ADDRESS, "Bridge: wrappedCurrency empty"), wrappedCurrency.deposit{ value: msg.value }(), crossTokens(address(wrappedCurrency), sender, to, msg.value, "")
  - 函数: tokensReceived
  - 关键操作: require(to == address(this), "Bridge: Not to this address"), require(erc1820.getInterfaceImplementer(tokenToUse, _erc777Interface) != NULL_ADDRESS, "Bridge: Not ERC777 token"), require(userData.length != 0 || !from.isContract(), "Bridge: Specify receiver address in data"), address receiver = userData.length == 0 ? from : LibUtils.bytesToAddress(userData), crossTokens(tokenToUse, from, receiver, amount, userData)
### rel_chain: relay_chain
- **事件**: Voted
  - 函数: voteTransaction
  - 关键操作: require(isMember[_msgSender()], "Federation: Not Federator"), bytes32 transactionId = getTransactionId(originalTokenAddress, sender, receiver, amount, blockHash, transactionHash, logIndex), if (processed[transactionId]) return true, if (votes[transactionId][_msgSender()]) return true, votes[transactionId][_msgSender()] = true, uint transactionCount = getTransactionCount(transactionId), if (transactionCount >= required && transactionCount >= members.length / 2 + 1), processed[transactionId] = true, bridge.acceptTransfer(originalTokenAddress, sender, receiver, amount, blockHash, transactionHash, logIndex)
- **事件**: Executed
  - 函数: acceptTransfer
  - 关键操作: require(_msgSender() == federation, "Bridge: Not Federation"), require(knownTokens[_originalTokenAddress] || mappedTokens[_originalTokenAddress] != NULL_ADDRESS, "Bridge: Unknown token"), require(_to != NULL_ADDRESS, "Bridge: Null To"), require(_amount > 0, "Bridge: Amount 0"), require(_blockHash != NULL_HASH, "Bridge: Null BlockHash"), require(_transactionHash != NULL_HASH, "Bridge: Null TxHash"), require(transactionsDataHashes[_transactionHash] == bytes32(0), "Bridge: Already accepted"), bytes32 _transactionDataHash = getTransactionDataHash(_to, _amount, _blockHash, _transactionHash, _logIndex), require(!claimed[_transactionDataHash], "Bridge: Already claimed"), transactionsDataHashes[_transactionHash] = _transactionDataHash, originalTokenAddresses[_transactionHash] = _originalTokenAddress, senderAddresses[_transactionHash] = _from
### det_chain: destination_chain
- **事件**: Claimed1
  - 函数: claim
  - 关键操作: receivedAmount = _claim(_claimData, _claimData.to, payable(address(0)), 0)
  - 函数: claimFallback
  - 关键操作: require(_msgSender() == senderAddresses[_claimData.transactionHash],"Bridge: invalid sender"), receivedAmount = _claim(_claimData, _msgSender(), payable(address(0)), 0)
  - 函数: claimGasless
  - 关键操作: require(_deadline >= block.timestamp, "Bridge: EXPIRED"), bytes32 digest = getDigest(_claimData, _relayer, _fee, _deadline), address recoveredAddress = ecrecover(digest, _v, _r, _s), require(_claimData.to != address(0) && recoveredAddress == _claimData.to, "Bridge: INVALID_SIGNATURE"), receivedAmount = _claim(_claimData, _claimData.to, _relayer, _fee)
---
