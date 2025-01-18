import { useModal } from "../../context/Modal";

function DeleteRecipeButton({
  modalComponent, // component to render inside the modal
  buttonImage, // image element for the button
  onButtonClick, // optional: callback function that will be called once the button that opens the modal is clicked
  onModalClose, // optional: callback function that will be called once the modal is closed
}) {
  const { setModalContent, setOnModalClose } = useModal();

  const onClick = () => {
    if (onModalClose) setOnModalClose(onModalClose);
    setModalContent(modalComponent);
    if (typeof onButtonClick === "function") onButtonClick();
  };

  return (
    <button onClick={onClick} className="delete-button">
      {buttonImage}
    </button>
  );
}

export default DeleteRecipeButton;
