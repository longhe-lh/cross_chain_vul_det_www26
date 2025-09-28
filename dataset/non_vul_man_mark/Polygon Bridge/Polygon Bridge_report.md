# 跨链桥合约分析报告
## 跨链桥: Polygon Bridge
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: depositEther1, depositERC202, depositERC7213
- **rel_chain**: submitHeaderBlock, submitCheckpoint
- **det_chain**: withdraw1, exitTokens2
### src_chain: Root Chain
- **事件**: depositEther1
  - 函数: depositEtherFor
  - 关键操作: require(stakeManager.delegationDeposit(validatorId, amountToDeposit, msg.sender), "deposit failed");, stakingLogger.logShareMinted(validatorId, user, _amount, shares);, stakingLogger.logStakeUpdate(validatorId);
- **事件**: depositERC202
  - 函数: depositERC20ForUser
  - 关键操作: require(_amount <= maxErc20Deposit, "exceed maximum deposit amount");, IERC20(_token).safeTransferFrom(msg.sender, address(this), _amount);, stakingLogger.logShareMinted(validatorId, user, _amount, shares);, stakingLogger.logStakeUpdate(validatorId);
- **事件**: depositERC7213
  - 函数: depositERC721ForUser
  - 关键操作: require(registry.isTokenMappedAndIsErc721(_token), "not erc721");, IERC721(_token).safeTransferFrom(msg.sender, address(this), _tokenId);, stakingLogger.logShareMinted(validatorId, user, _amount, shares);, stakingLogger.logStakeUpdate(validatorId);
### rel_chain: Relay Chain
- **事件**: submitHeaderBlock
  - 函数: submitHeaderBlock
  - 关键操作: require(CHAINID == _borChainID, "Invalid bor chain id");, require(_buildHeaderBlock(proposer, start, end, rootHash), "INCORRECT_HEADER_DATA");, uint256 _reward = stakeManager.checkSignatures(end.sub(start).add(1), keccak256(abi.encodePacked(bytes(hex"01"), data)), accountHash, proposer, sigs);, require(_reward != 0, "Invalid checkpoint");, emit NewHeaderBlock(proposer, _nextHeaderBlock, _reward, start, end, rootHash);, _nextHeaderBlock = _nextHeaderBlock.add(MAX_DEPOSITS);, _blockDepositId = 1;
- **事件**: submitCheckpoint
  - 函数: submitCheckpoint
  - 关键操作: require(CHAINID == _borChainID, "Invalid bor chain id");, require(_buildHeaderBlock(proposer, start, end, rootHash), "INCORRECT_HEADER_DATA");, uint256 _reward = stakeManager.checkSignatures(end.sub(start).add(1), keccak256(abi.encodePacked(bytes(hex"01"), data)), accountHash, proposer, sigs);, require(_reward != 0, "Invalid checkpoint");, emit NewHeaderBlock(proposer, _nextHeaderBlock, _reward, start, end, rootHash);, _nextHeaderBlock = _nextHeaderBlock.add(MAX_DEPOSITS);, _blockDepositId = 1;
### det_chain: Child Chain
- **事件**: withdraw1
  - 函数: withdraw
  - 关键操作: require(isContract(_newProxyTo), "DESTINATION_ADDRESS_IS_NOT_A_CONTRACT");, address predicateAddress = typeToPredicate[tokenType];, require(predicateAddress != address(0), "INVALID_TOKEN_TYPE");, require(user != address(0), "INVALID_USER");, ITokenPredicate(predicateAddress).lockTokens(_msgSender(), user, rootToken, depositData);, bytes memory syncData = abi.encode(user, rootToken, depositData);, stateSender.syncState(childChain, abi.encode(DEPOSIT, syncData));, emit NewDepositBlock(_user, _token, _amountOrToken, _depositId);
- **事件**: exitTokens2
  - 函数: exitTokens
  - 关键操作: require(rootToChildTokens[rootToken] == childToken, "INVALID_MAPPING_ON_EXIT");, ERC1155(rootToken).safeTransferFrom(address(this), user, id, amount, data);, emit FxWithdrawMintableERC1155(rootToken, childToken, user, id, amount);
---
